from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional

@dataclass
class FileInfo:
    path: Path
    rel_path: str
    name: str
    ext: str
    starred: bool = False
    imports: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)

@dataclass
class FolderNode:
    path: Path
    rel_path: str
    name: str
    files: List[FileInfo] = field(default_factory=list)
    subfolders: Dict[str, 'FolderNode'] = field(default_factory=dict)
    description: Optional[str] = None

    def add_file(self, file_info: FileInfo):
        self.files.append(file_info)

    def get_or_create_subfolder(self, path: Path, rel_path: str) -> 'FolderNode':
        if rel_path not in self.subfolders:
            self.subfolders[rel_path] = FolderNode(path=path, rel_path=rel_path, name=path.name)
        return self.subfolders[rel_path]
