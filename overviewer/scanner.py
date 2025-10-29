from __future__ import annotations
from pathlib import Path
from typing import Iterable, Dict, Tuple, Optional, List
import os
import ast

from .model import FolderNode, FileInfo
from .filters import should_ignore_dir, should_ignore_file, AUTO_STAR_FILENAMES, is_binary_ext
from .cache import load_cache, save_cache

PYTHON_EXTS = {'.py'}
TS_EXTS = {'.ts', '.tsx'}
JS_EXTS = {'.js', '.jsx'}
CSHARP_EXT = '.cs'
JAVA_EXT = '.java'

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
            # split grouped exports
            for part in m2.split(','):
                pname = part.strip().split(' as ')[0]
                if pname:
                    exports.append(pname)
    return imports, functions, classes, exports

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
            if include_exts and ext not in include_exts:
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
                            imports, functions, classes, exports = extract_ts_js_info(text)
                        else:
                            imports, functions, _, _ = extract_ts_js_info(text)
                    elif ext == CSHARP_EXT or ext == JAVA_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        if not enrich_languages or enrich_languages.get('cstyle', True):
                            imports, functions, classes, exports, doc_summary = extract_cstyle_info(text)
                        else:
                            imports, functions, _, _, _ = extract_cstyle_info(text)
                if mtime is not None:
                    updated_cache[rel_key] = {
                        'mtime': mtime,
                        'imports': imports,
                        'functions': functions,
                        'classes': classes,
                        'exports': exports,
                        'doc_summary': doc_summary
                    }
            # line count
            line_count = 0
            if not skipped:
                try:
                    with path.open('r', encoding='utf-8', errors='ignore') as fh:
                        line_count = sum(1 for _ in fh)
                except Exception:
                    line_count = 0
            fi = FileInfo(path=path, rel_path=rel_key, name=filename, ext=ext, starred=starred, imports=imports, functions=functions,
                          line_count=line_count, classes=classes, exports=exports, doc_summary=doc_summary or None, skipped=skipped)
            current_folder.add_file(fi)
    if use_cache:
        save_cache(root, {'files': updated_cache})
    return project
