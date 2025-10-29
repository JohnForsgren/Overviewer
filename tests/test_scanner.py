from pathlib import Path
from overviewer.scanner import scan_project
from overviewer.renderer import render_markdown, MODE_AI, MODE_DEVELOPER

DATA_DIR = Path(__file__).parent / 'data'


def test_scan_python_and_ts():
    tree = scan_project(DATA_DIR, include_exts=['.py', '.tsx'])
    md_dev = render_markdown(tree, mode=MODE_DEVELOPER)
    md_ai = render_markdown(tree, mode=MODE_AI)
    # Basic assertions
    assert 'sample.py' in md_dev
    assert 'App.tsx' in md_ai
    # AI mode should include info lines
    assert 'Imports:' in md_ai
    assert 'Functions:' in md_ai


def test_auto_star():
    tree = scan_project(DATA_DIR, include_exts=['.tsx'])
    md = render_markdown(tree, mode=MODE_DEVELOPER)
    assert '⭐️ App.tsx' in md


def test_headings_present():
    tree = scan_project(DATA_DIR, include_exts=['.py'])
    md = render_markdown(tree, mode=MODE_DEVELOPER)
    # Root heading without hash
    assert '======= 📁' in md
    # No raw hash heading markers should appear now
    assert '# 📁' not in md and '## 📁' not in md and '### ' not in md
