from __future__ import annotations
from pathlib import Path
from typing import List
import re

from .model import FolderNode

FOLDER_HEADING_RE = re.compile(
    r"^(?:#\s+={7}\s+📁\s+(.+?)/\s+={7}|#\s+={3}\s+📁\s+(.+?)/\s+={3}|\s*(#{3,})\s+📁\s+(.+?)/)\s*$"
)


def parse_blueprint(path: Path) -> List[str]:
    """Parse existing blueprint markdown; return list of folder paths referenced.
    (Simplified: we only extract folder rel paths.)"""
    text = path.read_text(encoding='utf-8', errors='ignore')
    folders = []
    for line in text.splitlines():
        stripped = line.rstrip()
        m = FOLDER_HEADING_RE.match(stripped)
        if m:
            g1, g2, g3, g4 = m.groups()
            rel = g1 or g2 or g4
            if rel:
                rel = rel.strip()
                if not rel.endswith('/'):
                    rel += '/'
                folders.append(rel)
    return folders
