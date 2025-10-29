from __future__ import annotations
import argparse
from pathlib import Path

from .scanner import scan_project
from .renderer import render_markdown, MODE_DEVELOPER, MODE_AI
from .interface import launch_gui
from .blueprint import parse_blueprint


def main():
    parser = argparse.ArgumentParser(description='Overviewer - generate codebase blueprint markdown.')
    sub = parser.add_subparsers(dest='command')

    scan_p = sub.add_parser('scan', help='Scan a project and output markdown')
    scan_p.add_argument('--root', required=True, help='Root directory of project')
    scan_p.add_argument('--mode', choices=[MODE_DEVELOPER, MODE_AI], default=MODE_DEVELOPER)
    scan_p.add_argument('--output', required=True, help='Output markdown file path')
    scan_p.add_argument('--ext', action='append', help='Limit to given extension(s), can repeat')

    gui_p = sub.add_parser('gui', help='Launch GUI interface')

    ingest_p = sub.add_parser('ingest-blueprint', help='Parse existing blueprint and rescan limited paths')
    ingest_p.add_argument('--root', required=True)
    ingest_p.add_argument('--blueprint', required=True)
    ingest_p.add_argument('--mode', choices=[MODE_DEVELOPER, MODE_AI], default=MODE_DEVELOPER)
    ingest_p.add_argument('--output', required=True)

    args = parser.parse_args()

    if args.command == 'gui':
        launch_gui()
        return

    if args.command == 'scan':
        tree = scan_project(Path(args.root), include_exts=args.ext)
        md = render_markdown(tree, mode=args.mode)
        Path(args.output).write_text(md, encoding='utf-8')
        print(f'Wrote blueprint to {args.output}')
        return

    if args.command == 'ingest-blueprint':
        folders = parse_blueprint(Path(args.blueprint))
        root = Path(args.root).resolve()
        tree = scan_project(root, include_exts=args.ext)
        # Filter tree to only included folders (simplified by just removing unmatched subfolders recursively)
        allowed = set(folders)

        def filter_folder(folder):
            folder.subfolders = {k: v for k, v in folder.subfolders.items() if (v.rel_path in allowed or any(v.rel_path.startswith(a) for a in allowed))}
            for sub in folder.subfolders.values():
                filter_folder(sub)
        filter_folder(tree)
        md = render_markdown(tree, mode=args.mode)
        Path(args.output).write_text(md, encoding='utf-8')
        print(f'Rescanned and wrote filtered blueprint to {args.output}')
        return

    parser.print_help()

if __name__ == '__main__':
    main()
