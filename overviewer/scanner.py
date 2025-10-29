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

def extract_python_info(path: Path) -> Tuple[Iterable[str], Iterable[str]]:
    try:
        tree = ast.parse(path.read_text(encoding='utf-8', errors='ignore'))
    except Exception:
        return [], []
    imports = []
    functions = []
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
    return imports, functions

# For TS/JS we do lightweight regex scanning
import re
TS_JS_IMPORT_RE = re.compile(r"import\s+(?:[^'\"]+from\s+)?['\"]([^'\"]+)['\"]")
TS_JS_FUNC_RE = re.compile(r"function\s+([a-zA-Z0-9_]+)|([a-zA-Z0-9_]+)\s*=\s*\([^)]*\)\s*=>")


def extract_ts_js_info(text: str):
    imports = TS_JS_IMPORT_RE.findall(text)
    imports = [m for m in imports if m]
    functions = []
    for match in TS_JS_FUNC_RE.findall(text):
        name = match[0] or match[1]
        if name:
            functions.append(name)
    return imports, functions

# For C# and Java (very light heuristic)
CSTYLE_IMPORT_RE = re.compile(r"using\s+([a-zA-Z0-9_.]+);|import\s+([a-zA-Z0-9_.]+);")
CSTYLE_FUNC_RE = re.compile(r"\b([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)\s*\([^;]*?\)\s*{")

def extract_cstyle_info(text: str):
    imports = []
    for a, b in CSTYLE_IMPORT_RE.findall(text):
        imports.append(a or b)
    functions = []
    for ret, name in CSTYLE_FUNC_RE.findall(text):
        functions.append(name)
    return imports, functions

# --- Core scanning ---

MAX_PARSE_SIZE = 400_000  # bytes: skip metadata parsing for very large files

def scan_project(root: Path, include_exts=None, use_cache: bool = False, parse_metadata: bool = True) -> FolderNode:
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
                except Exception:
                    pass
            if parse_this:
                cached_entry = file_cache.get(rel_key) if (mtime is not None and use_cache) else None
                if cached_entry and cached_entry.get('mtime') == mtime:
                    imports = cached_entry.get('imports', [])
                    functions = cached_entry.get('functions', [])
                else:
                    if ext in PYTHON_EXTS:
                        imports, functions = extract_python_info(path)
                    elif ext in TS_EXTS or ext in JS_EXTS:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions = extract_ts_js_info(text)
                    elif ext == CSHARP_EXT or ext == JAVA_EXT:
                        text = path.read_text(encoding='utf-8', errors='ignore')
                        imports, functions = extract_cstyle_info(text)
                if mtime is not None:
                    updated_cache[rel_key] = {
                        'mtime': mtime,
                        'imports': imports,
                        'functions': functions
                    }
            fi = FileInfo(path=path, rel_path=rel_key, name=filename, ext=ext, starred=starred, imports=imports, functions=functions)
            current_folder.add_file(fi)
    if use_cache:
        save_cache(root, {'files': updated_cache})
    return project
