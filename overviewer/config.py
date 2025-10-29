from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

CONFIG_FILENAME = '.overviewer_config.json'


def load_config(root: Path) -> Dict[str, Any]:
    cfg_path = root / CONFIG_FILENAME
    if not cfg_path.exists():
        return {}
    try:
        return json.loads(cfg_path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_config(root: Path, data: Dict[str, Any]):
    cfg_path = root / CONFIG_FILENAME
    try:
        cfg_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    except Exception:
        pass
