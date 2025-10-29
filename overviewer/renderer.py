from __future__ import annotations
from pathlib import Path
from typing import List

from .model import FolderNode, FileInfo

MODE_DEVELOPER = 'developer'
MODE_AI = 'ai'

SYMBOL_FOLDER = '📁'
SYMBOL_DESC = '📄'
SYMBOL_STAR = '⭐️'
SYMBOL_INFO = '📕'
SYMBOL_AI = '🤖'
SYMBOL_BRAIN = '🧠'


def render_markdown(root: FolderNode, mode: str = MODE_DEVELOPER) -> str:
    """Render markdown with hash symbols removed from folder headings:
    Depth 1: ======= 📁 path/ =======
    Depth 2: === 📁 path/ ===
    Depth 3: 📁 path/
    Depth >=4: (depth-3)*4 spaces + 📁 path/
    Files: star at start if starred.
    """
    lines: List[str] = []

    def heading_line(folder: FolderNode, depth: int) -> str:
        rel = folder.rel_path if folder.rel_path.endswith('/') else folder.rel_path + '/'
        if depth == 1:
            return f"{'='*7} {SYMBOL_FOLDER} {rel} {'='*7}"
        if depth == 2:
            return f"{'='*3} {SYMBOL_FOLDER} {rel} {'='*3}"
        if depth == 3:
            return f"{SYMBOL_FOLDER} {rel}"
        indent = ' ' * ((depth - 3) * 4)
        return f"{indent}{SYMBOL_FOLDER} {rel}"

    def file_indent(depth: int) -> str:
        if depth <= 2:
            return ''
        return ' ' * ((depth - 2) * 4)

    def meta_indent(depth: int) -> str:
        return file_indent(depth) + (' ' * 4 if depth > 2 else '    ')

    def walk(folder: FolderNode, depth: int = 1):
        lines.append(heading_line(folder, depth))
        desc_indent = file_indent(depth)
        lines.append(f"{desc_indent}{SYMBOL_DESC} Description:")
        indent = file_indent(depth)
        for fi in sorted(folder.files, key=lambda f: f.name.lower()):
            prefix = f"{SYMBOL_STAR} " if fi.starred else ''
            lines.append(f"{indent}{prefix}{fi.name}")
            if mode == MODE_AI and fi.enriched:
                mid = meta_indent(depth)
                if fi.skipped:
                    lines.append(f"{mid}{SYMBOL_INFO} Skipped: large file")
                else:
                    if fi.imports:
                        lines.append(f"{mid}{SYMBOL_INFO} Imports: {', '.join(fi.imports[:25])}")
                    if fi.functions:
                        lines.append(f"{mid}{SYMBOL_INFO} Functions: {', '.join(fi.functions[:25])}")
                    if fi.classes:
                        lines.append(f"{mid}{SYMBOL_INFO} Classes: {', '.join(fi.classes[:10])}")
                    if fi.exports:
                        lines.append(f"{mid}{SYMBOL_INFO} Exports: {', '.join(fi.exports[:10])}")
                    if fi.line_count:
                        lines.append(f"{mid}{SYMBOL_INFO} Stats: LOC {fi.line_count} | funcs {len(fi.functions)} | classes {len(fi.classes)} | exports {len(fi.exports)}")
                    if fi.doc_summary:
                        lines.append(f"{mid}{SYMBOL_INFO} Doc: {fi.doc_summary}")
        for sub in sorted(folder.subfolders.values(), key=lambda s: s.name.lower()):
            walk(sub, depth + 1)

    walk(root, 1)
    return '\n'.join(lines).rstrip() + '\n'
