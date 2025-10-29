# Overviewer Project Documentation (Concise Context)

## Feature Summary
Core purpose: Generate a structured, human‑readable Markdown “blueprint” of a source tree for fast onboarding (Developer mode) or richer semantic context (AI mode) while staying performant on large repos.

Features:
- Project scan of directory tree with ignore rules (e.g. node_modules, venv, dist, build, __pycache__, .git, binary/asset directories).
- Dynamic extension discovery: first scan collects all encountered file extensions; user can toggle which extensions to include for subsequent metadata parsing.
- Two modes:
	- Developer mode: compact listing with file names and placeholder descriptions.
	- AI mode: adds extracted imports and function names per file (heuristic + AST for Python, regex heuristics for others) with capped lists for performance.
- Hashless hierarchical folder headings: decorative top (root) and second level using equals framing; deeper levels plain with indentation spacing.
- Star highlighting: important/framework entry files (e.g. App.*, index.*, main.*) automatically prefixed with a star symbol.
- Caching: JSON cache keyed by file path + mtime to avoid re‑parsing unchanged files (imports/functions) on subsequent scans.
- Config persistence: extension toggle states saved per root for consistent UX across sessions.
- Performance optimizations: directory pruning, binary extension skipping, file size guard, metadata only for selected extensions after initial pass.
- GUI (Tkinter): threaded background scan with modal progress window (no UI freeze), colorization of file lines by extension (auto‑enabled, toggle button), file counts per extension shown under each checkbox, live object counts (files/folders) after scan.
- CLI entrypoint: scan rendering and blueprint ingestion via arguments.
- Blueprint ingestion: parse existing blueprint to focus future scans (regex of heading patterns) – currently adapted for hashless headings.
- Deterministic color palette applied to file lines by extension; recolorable on demand.
- Clean indentation rules: 4 spaces per deeper hierarchy level; aligned metadata lines beneath files in AI mode.

## Code Structure (One‑Line Per File)
- `overviewer/__init__.py` – Exposes primary API functions (scan, render, parse blueprint) for external use.
- `overviewer/model.py` – Dataclasses for `FileInfo` and `FolderNode` representing the scanned tree and file metadata.
- `overviewer/filters.py` – Directory & file ignore logic, binary extension list, and automatic star filename heuristics.
- `overviewer/scanner.py` – Core recursive project traversal, extension discovery, metadata parsing (AST/regex), caching integration.
- `overviewer/renderer.py` – Markdown assembly: heading formatting (hashless), indentation, star placement, optional AI metadata blocks.
- `overviewer/blueprint.py` – Parses existing blueprint headings to constrain subsequent scans to specified subtrees.
- `overviewer/cache.py` – Load/save JSON metadata cache keyed by relative file path and modification time.
- `overviewer/config.py` – Load/save per‑project configuration (enabled extensions, future toggles) to a JSON file.
- `overviewer/interface.py` – Tkinter GUI: root selection, scan orchestration (threaded), extension toggles with counts, colorization, save output.
- `overviewer/__main__.py` – CLI entry (scan, gui, ingest-blueprint) using argparse.
- `tests/test_scanner.py` – Unit tests validating scanning, rendering (star placement, heading format), and AI metadata presence.
- `Project_Documentation/Project_Documentation.md` – (This file) Concise reference of features and internal structure for quick ramp‑up.

## High-Level Flow
1. User selects root (GUI) or passes via CLI.
2. Initial scan builds folder tree + extension set (lightweight metadata or none for speed).
3. Extensions are toggled; second scan (if needed) parses imports/functions only for selected types using cache to skip unchanged files.
4. Renderer produces Markdown with consistent formatting (hashless headings) and file/star markers; AI mode inserts metadata lines.
5. GUI optionally colorizes file lines and shows counts; user saves Markdown or re‑scans with new toggles.

## Notes
- Large binary or oversized source files are skipped from deep parsing to preserve responsiveness.
- Colorization and formatting do not alter underlying output semantics (safe for ingestion by tooling expecting plain text).
- The design aims to keep tests minimal but focused on structural guarantees (presence of core markers, star symbol, headings).

