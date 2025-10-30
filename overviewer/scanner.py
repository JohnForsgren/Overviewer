from __future__ import annotations
from pathlib import Path
from typing import Iterable, Dict, Tuple, Optional, List
import os
import ast

from .model import FolderNode, FileInfo
from .filters import should_ignore_dir, should_ignore_file, AUTO_STAR_FILENAMES, is_binary_ext, is_excluded_structure_ext
from .cache import load_cache, save_cache

PYTHON_EXTS = {'.py'}
TS_EXTS = {'.ts', '.tsx'}
JS_EXTS = {'.js', '.jsx'}
CSHARP_EXT = '.cs'
JAVA_EXT = '.java'
SHELL_EXT = '.sh'
XSL_EXT = '.xsl'
XML_EXT = '.xml'
# DITA support disabled (no enrichment / parsing) per requirement; keep constant for potential future restore
DITA_EXTS = {'.dita', '.ditamap'}
SCSS_EXT = '.scss'
CSS_EXT = '.css'

# --- Parsing helpers ---

def extract_python_info(path: Path) -> Tuple[List[str], List[str], List[str], List[str], str]:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(text)
    except Exception:
        return [], [], [], [], ''
    imports: List[str] = []
    functions: List[str] = []
    classes: List[str] = []
    exports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            else:
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    # Exports via __all__ or default to top-level defs
    all_names = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    try:
                        if isinstance(node.value, (ast.List, ast.Tuple)):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    all_names.append(elt.value)
                    except Exception:
                        pass
    if all_names:
        exports = all_names
    else:
        # naive export assumption: all top-level functions/classes
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                exports.append(getattr(n, 'name', ''))
    doc = ast.get_docstring(tree) or ''
    doc_first = ''
    if doc:
        doc_first = doc.strip().split('\n')[0][:500]
    return imports, functions, classes, exports, doc_first
    return imports, functions

# For TS/JS we do lightweight regex scanning
import re
TS_JS_IMPORT_RE = re.compile(r"import\s+(?:[^'\"]+from\s+)?['\"]([^'\"]+)['\"]")
TS_JS_FUNC_RE = re.compile(r"function\s+([a-zA-Z0-9_]+)|([a-zA-Z0-9_]+)\s*=\s*\([^)]*\)\s*=>")
EXPORT_TS_JS_RE = re.compile(r"export\s+(?:default\s+)?(?:class|function|const|let|var)\s+([A-Za-z0-9_]+)|export\s*{\s*([^}]+)\s*}")
CLASS_TS_JS_RE = re.compile(r"class\s+([A-Za-z0-9_]+)")
EXPORT_TS_TYPE_RE = re.compile(r"export\s+(?:type|interface|enum)\s+([A-Za-z0-9_]+)")
TS_DOC_BLOCK_RE = re.compile(r"/\*\*([^*]|\*(?!/))*\*/", re.DOTALL)

def _summarize_ts_js_doc(text: str) -> str:
    """Return first sentence of first JSDoc-style block."""
    match = TS_DOC_BLOCK_RE.search(text)
    if not match:
        return ''
    block = match.group(0)
    # Remove /** */ markers
    inner = re.sub(r"^/\*\*|\*/$", "", block).strip()
    # Strip leading *
    inner = re.sub(r"^\s*\*\s?", "", inner, flags=re.MULTILINE)
    # First line / sentence
    first_line = inner.split('\n')[0].strip()
    return first_line[:500]

def extract_ts_js_info(text: str):
    imports_raw = TS_JS_IMPORT_RE.findall(text)
    imports = [m for m in imports_raw if m]
    functions: List[str] = []
    for match in TS_JS_FUNC_RE.findall(text):
        name = match[0] or match[1]
        if name:
            functions.append(name)
    classes = CLASS_TS_JS_RE.findall(text)
    exports: List[str] = []
    for m1, m2 in EXPORT_TS_JS_RE.findall(text):
        if m1:
            exports.append(m1)
        elif m2:
            for part in m2.split(','):
                pname = part.strip().split(' as ')[0]
                if pname:
                    exports.append(pname)
    # type/interface/enum exports
    type_exports = EXPORT_TS_TYPE_RE.findall(text)
    # Deduplicate while preserving order
    seen = set()
    dedup_exports: List[str] = []
    for e in exports:
        if e not in seen:
            seen.add(e)
            dedup_exports.append(e)
    # Append type exports distinctly (avoid collisions)
    for te in type_exports:
        if te not in seen:
            seen.add(te)
            dedup_exports.append(te + " (type)")
    doc_summary = _summarize_ts_js_doc(text)
    return imports, functions, classes, dedup_exports, doc_summary

# For C# and Java (very light heuristic)
CSTYLE_IMPORT_RE = re.compile(r"using\s+([a-zA-Z0-9_.]+);|import\s+([a-zA-Z0-9_.]+);")
CSTYLE_FUNC_RE = re.compile(r"\b([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)\s*\([^;]*?\)\s*{")

CLASS_CSTYLE_RE = re.compile(r"\bclass\s+([A-Za-z0-9_]+)")
PUBLIC_EXPORT_RE = re.compile(r"public\s+(?:class|static\s+)?([A-Za-z0-9_]+)")

def extract_cstyle_info(text: str):
    imports = []
    for a, b in CSTYLE_IMPORT_RE.findall(text):
        imports.append(a or b)
    functions = []
    for ret, name in CSTYLE_FUNC_RE.findall(text):
        functions.append(name)
    classes = CLASS_CSTYLE_RE.findall(text)
    exports = []
    for exp in PUBLIC_EXPORT_RE.findall(text):
        exports.append(exp)
    # Doc summary: first block or line comment group
    doc_summary = ''
    doc_match = re.search(r"/\*\*(.*?)\*/", text, re.DOTALL) or re.search(r"/\*(.*?)\*/", text, re.DOTALL)
    if doc_match:
        raw = doc_match.group(1).strip().split('\n')[0]
        doc_summary = raw[:500]
    else:
        line_comments = re.findall(r"^(?:\s*//\s*(.+))$", text, re.MULTILINE)
        if line_comments:
            doc_summary = line_comments[0].strip()[:500]
    return imports, functions, classes, exports, doc_summary

# --- Additional language/group helpers ---

SHELL_FUNC_RE = re.compile(r"^([A-Za-z0-9_]+)\s*\(\)\s*{", re.MULTILINE)
SHELL_SOURCE_RE = re.compile(r"^\s*(?:source|\.)\s+(['\"]?)([^'\"\s]+)\1", re.MULTILINE)
SHELL_SHEBANG_RE = re.compile(r"^#!(.+)$", re.MULTILINE)

def extract_shell_info(text: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    # Shell: treat sourced files as imports, functions via name() {, no classes/exports
    shebang_match = SHELL_SHEBANG_RE.search(text)
    shebang = shebang_match.group(1).strip() if shebang_match else ''
    sourced = [m[1] for m in SHELL_SOURCE_RE.findall(text)]
    funcs = SHELL_FUNC_RE.findall(text)
    doc_summary = ''
    # Multi-line top comment block (excluding shebang). Collect contiguous # lines.
    lines = text.splitlines()
    comment_block: List[str] = []
    started = False
    for line in lines:
        if line.startswith('#') and not line.startswith('#!'):
            comment_block.append(line.lstrip('#').strip())
            started = True
        elif started:
            break
    if comment_block:
        joined = ' '.join(comment_block).strip()
        doc_summary = joined[:500]
    imports = []
    if shebang:
        imports.append(f"shebang:{shebang}")
    imports.extend(sourced)
    # Star heuristic handled outside (filename check)
    return imports, funcs, [], [], doc_summary

XSL_TEMPLATE_RE = re.compile(r"<xsl:template[^>]*name=\"([^\"]+)\"", re.IGNORECASE)
XSL_MATCHED_TEMPLATE_RE = re.compile(r"<xsl:template[^>]*match=\"([^\"]+)\"", re.IGNORECASE)
XSL_IMPORT_RE = re.compile(r"<xsl:(?:import|include)\s+href=\"([^\"]+)\"", re.IGNORECASE)

XSL_FUNCTION_RE = re.compile(r"<xsl:function[^>]*name=\"([^\"]+)\"", re.IGNORECASE)

def extract_xsl_info(text: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    named_templates = XSL_TEMPLATE_RE.findall(text)
    matched_templates = XSL_MATCHED_TEMPLATE_RE.findall(text)
    fn_functions = XSL_FUNCTION_RE.findall(text)
    imports = XSL_IMPORT_RE.findall(text)
    # Only treat named templates and xsl:function as 'functions'; matched templates summarized
    functions = named_templates + fn_functions
    doc_summary = ''
    first_stylesheet = re.search(r"<xsl:stylesheet[^>]*>", text, re.IGNORECASE)
    if first_stylesheet:
        head = first_stylesheet.group(0)
        # Collapse internal whitespace/newlines for readability and append counts comma-separated
        compact = re.sub(r"\s+", " ", head).strip()
        counts = f"named_templates:{len(named_templates)}, match_templates:{len(matched_templates)}, functions:{len(fn_functions)}"
        doc_summary = f"{compact} {counts}"[:500]
    return imports, functions, [], [], doc_summary

XML_ROOT_RE = re.compile(r"<([A-Za-z0-9_:-]+)(?:\s|>)")
XML_NS_RE = re.compile(r"xmlns(?::[A-Za-z0-9_-]+)?=\"[^\"]+\"")

def extract_xml_info(text: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    root_match = XML_ROOT_RE.search(text)
    root = root_match.group(1) if root_match else ''
    namespaces = XML_NS_RE.findall(text)
    # Deduplicate namespaces
    unique_ns = []
    seen_ns = set()
    for ns in namespaces:
        if ns not in seen_ns:
            seen_ns.add(ns)
            unique_ns.append(ns)
    tags = set(re.findall(r"<([A-Za-z0-9_:-]+)", text))
    doc_summary = ''
    if root:
        doc_summary = f"root:{root} tags:{len(tags)}"[:500]
    imports = unique_ns  # treat namespaces as imports for context
    return imports, [], [], [], doc_summary

DITA_KEYREF_RE = re.compile(r"keyref=\"([^\"]+)\"")
DITA_HREF_RE = re.compile(r"href=\"([^\"]+)\"")

def extract_dita_info(text: str, ext: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    root_match = XML_ROOT_RE.search(text)
    root = root_match.group(1) if root_match else ''
    keyrefs = DITA_KEYREF_RE.findall(text)
    hrefs = DITA_HREF_RE.findall(text)
    doc_summary = ''
    if root:
        doc_summary = f"root:{root} keyrefs:{len(keyrefs)} hrefs:{len(hrefs)}"[:500]
    imports = keyrefs  # expose keyrefs
    functions: List[str] = []
    return imports, functions, [], [], doc_summary

SCSS_VAR_RE = re.compile(r"\$([A-Za-z0-9_-]+):")
SCSS_MIXIN_RE = re.compile(r"@mixin\s+([A-Za-z0-9_-]+)")
SCSS_SELECTOR_RE = re.compile(r"^[^{]+{", re.MULTILINE)

def extract_scss_info(text: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    vars_found = SCSS_VAR_RE.findall(text)
    mixins = SCSS_MIXIN_RE.findall(text)
    selectors = SCSS_SELECTOR_RE.findall(text)
    doc_summary = f"vars:{len(vars_found)} mixins:{len(mixins)} selectors:{len(selectors)}"[:500]
    imports: List[str] = []
    # @use and @import directives
    for m in re.findall(r"@(use|import)\s+['\"]([^'\"]+)['\"]", text):
        imports.append(m[1])
    # treat mixins as functions
    functions = mixins
    return imports, functions, [], [], doc_summary

CSS_SELECTOR_RE = re.compile(r"^[^{]+{", re.MULTILINE)
CSS_MEDIA_RE = re.compile(r"@media\s+([^{]+){", re.IGNORECASE)
CSS_CUSTOM_PROP_RE = re.compile(r"--[A-Za-z0-9_-]+\s*:")
CSS_KEYFRAMES_RE = re.compile(r"@keyframes\s+([A-Za-z0-9_-]+)")

def extract_css_info(text: str) -> Tuple[List[str], List[str], List[str], List[str], str]:
    selectors = CSS_SELECTOR_RE.findall(text)
    medias = CSS_MEDIA_RE.findall(text)
    custom_props = CSS_CUSTOM_PROP_RE.findall(text)
    keyframes = CSS_KEYFRAMES_RE.findall(text)
    doc_summary = f"selectors:{len(selectors)} media_queries:{len(medias)} custom_props:{len(custom_props)} keyframes:{len(keyframes)}"[:500]
    return [], [], [], [], doc_summary

# --- Core scanning ---

MAX_PARSE_SIZE = 400_000  # bytes: skip metadata parsing for very large files

def scan_project(root: Path, include_exts=None, use_cache: bool = False, parse_metadata: bool = True, enrich_languages: Optional[Dict[str, bool]] = None) -> FolderNode:
    root = root.resolve()
    if include_exts is not None:
        include_exts = {e.lower() for e in include_exts}
    project = FolderNode(path=root, rel_path=root.name + '/', name=root.name)
    cache_data = load_cache(root) if use_cache else {}
    file_cache = cache_data.get('files', {}) if cache_data else {}
    updated_cache = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs in-place for efficiency
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d)]
        current_dir_path = Path(dirpath)
        rel_dir = current_dir_path.relative_to(root)
        # ensure folder node
        if rel_dir == Path('.'):
            current_folder = project
        else:
            cumulative = Path('')
            current_folder = project
            for part in rel_dir.parts:
                cumulative = cumulative / part
                current_folder = current_folder.get_or_create_subfolder(root / cumulative, cumulative.as_posix() + '/')
        for filename in filenames:
            path = current_dir_path / filename
            if should_ignore_file(path):
                continue
            ext = path.suffix.lower()
            # If include_exts was provided but is empty, skip all files (user deselected all types)
            if include_exts is not None:
                if len(include_exts) == 0:
                    continue
                if ext not in include_exts:
                    continue
            # Structural exclusion check
            if is_excluded_structure_ext(ext):
                continue
            rel = path.relative_to(root)
            starred = filename in AUTO_STAR_FILENAMES
            imports: List[str] = []
            functions: List[str] = []
            classes: List[str] = []
            exports: List[str] = []
            doc_summary: str = ''
            skipped = False
            rel_key = rel.as_posix()
            mtime = None
            try:
                mtime = path.stat().st_mtime
            except Exception:
                pass
            parse_this = parse_metadata and (include_exts is None or ext in include_exts) and not is_binary_ext(ext)
            if parse_this:
                # Size guard
                try:
                    if path.stat().st_size > MAX_PARSE_SIZE:
                        parse_this = False
                        skipped = True
                except Exception:
                    pass
            if parse_this:
                cached_entry = file_cache.get(rel_key) if (mtime is not None and use_cache) else None
                if cached_entry and cached_entry.get('mtime') == mtime:
                    imports = cached_entry.get('imports', [])
                    functions = cached_entry.get('functions', [])
                    classes = cached_entry.get('classes', [])
                    exports = cached_entry.get('exports', [])
                    doc_summary = cached_entry.get('doc_summary', '')
                else:
                    if ext in PYTHON_EXTS:
                        if not enrich_languages or enrich_languages.get('python', True):
                            imports, functions, classes, exports, doc_summary = extract_python_info(path)
                        else:
                            imports, functions, _, _, _ = extract_python_info(path)  # still need base imports/functions
                    elif ext in TS_EXTS or ext in JS_EXTS:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        if not enrich_languages or enrich_languages.get('ts_js', True):
                            imports, functions, classes, exports, doc_summary = extract_ts_js_info(text)
                        else:
                            imports, functions, classes, exports, doc_summary = extract_ts_js_info(text)
                    elif ext == CSHARP_EXT or ext == JAVA_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        if not enrich_languages or enrich_languages.get('cstyle', True):
                            imports, functions, classes, exports, doc_summary = extract_cstyle_info(text)
                        else:
                            imports, functions, _, _, _ = extract_cstyle_info(text)
                    elif ext == SHELL_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions, classes, exports, doc_summary = extract_shell_info(text)
                        # star heuristic for critical scripts
                        if any(k in filename.lower() for k in ('deploy', 'start', 'run')):
                            starred = True
                    elif ext == XSL_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions, classes, exports, doc_summary = extract_xsl_info(text)
                    # DITA parsing disabled intentionally; treat as simple text files (no metadata)
                    elif ext in DITA_EXTS:
                        pass  # skip metadata extraction for .dita / .ditamap
                    elif ext == SCSS_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions, classes, exports, doc_summary = extract_scss_info(text)
                    elif ext == CSS_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions, classes, exports, doc_summary = extract_css_info(text)
                    elif ext == XML_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions, classes, exports, doc_summary = extract_xml_info(text)
                # Vendor/minified heuristic
                vendor = False
                try:
                    size_bytes = path.stat().st_size
                    if ('.min.' in filename) or (ext in {'.js', '.css'} and size_bytes > 50_000 and line_count <= 10):
                        vendor = True
                except Exception:
                    pass
                if vendor and not doc_summary:
                    doc_summary = 'vendor:minified file (overview simplified)'
                if mtime is not None:
                    updated_cache[rel_key] = {
                        'mtime': mtime,
                        'imports': imports,
                        'functions': functions,
                        'classes': classes,
                        'exports': exports,
                        'doc_summary': doc_summary
                    }
            # line count only when enriching metadata
            line_count = 0
            if parse_metadata and not skipped:
                try:
                    with path.open('r', encoding='utf-8', errors='ignore') as fh:
                        line_count = sum(1 for _ in fh)
                except Exception:
                    line_count = 0
            fi = FileInfo(path=path, rel_path=rel_key, name=filename, ext=ext, starred=starred, imports=imports, functions=functions,
                          line_count=line_count, classes=classes, exports=exports, doc_summary=doc_summary or None, skipped=skipped,
                          enriched=parse_metadata)
            current_folder.add_file(fi)
    if use_cache:
        save_cache(root, {'files': updated_cache})
    return project
