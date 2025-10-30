from __future__ import annotations
from pathlib import Path
from typing import Set

DEFAULT_IGNORE_DIRS: Set[str] = {
    'node_modules', '.git', '.venv', 'venv', '__pycache__', 'dist', 'build', 'bin', 'obj', '.idea', '.vscode',
    'jre', 'fonts', 'font', 'assets', 'asset'
}

DEFAULT_IGNORE_FILE_PATTERNS: Set[str] = {
    '.DS_Store'
}

# Supported source extensions (initial scope)
SOURCE_EXTS: Set[str] = {
    '.ts', '.tsx', '.js', '.jsx', '.py', '.cs', '.java'
}

# Extensions typically not useful for overview (treated as binary/assets) - skipped for metadata parsing
# Binary/asset extensions: skipped for metadata parsing (but may still appear structurally unless excluded separately)
BINARY_EXTS: Set[str] = {
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.zip', '.jar', '.so', '.mp4', '.mp3', '.wav',
    '.ttf', '.otf', '.woff', '.woff2', '.dtd', '.ent', '.mod'
}

# Structural exclusion: do not list these files at all (suppressed in overview)
EXCLUDED_STRUCTURE_EXTS: Set[str] = {
    '.png', '.svg', '.jar', '.dtd', '.ent', '.mod'
}

TEXTLIKE_EXTS: Set[str] = {
    '.md', '.json', '.yml', '.yaml'
}

AUTO_STAR_FILENAMES = {
    'App.tsx', 'index.tsx', 'main.py', 'Program.cs', 'Main.java'
}

def should_ignore_dir(dir_name: str) -> bool:
    return dir_name in DEFAULT_IGNORE_DIRS

def should_ignore_file(path: Path) -> bool:
    if path.name in DEFAULT_IGNORE_FILE_PATTERNS:
        return True
    return False

def is_binary_ext(ext: str) -> bool:
    return ext.lower() in BINARY_EXTS

def is_excluded_structure_ext(ext: str) -> bool:
    return ext.lower() in EXCLUDED_STRUCTURE_EXTS

