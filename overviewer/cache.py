from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Tuple, Iterable

CACHE_FILENAME = '.overviewer_cache.json'


def load_cache(root: Path) -> Dict[str, Any]:
    path = root / CACHE_FILENAME
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_cache(root: Path, cache: Dict[str, Any]):
    path = root / CACHE_FILENAME
    try:
        path.write_text(json.dumps(cache, indent=2), encoding='utf-8')
    except Exception:
        pass
