# Overviewer Project Documentation (Concise Context)

## Feature Summary
Core purpose: Generate a structured, human‑readable Markdown “blueprint” of a source tree for fast onboarding (Developer mode) or richer semantic context (AI mode) while staying performant on large repos.

Features:
- Two‑phase scanning workflow: (1) Structure scan builds hierarchy only; (2) Enrichment pass adds rich metadata on demand.
- Project scan of directory tree with ignore rules (e.g. node_modules, venv, dist, build, __pycache__, .git, binary/asset directories).
- Dynamic extension discovery: first scan collects encountered extensions; user can toggle which to display/enrich.
- Modes:
  - Developer mode (future trim target): minimal hierarchy.
  - AI mode (default): supports enrichment with rich per‑file metadata.
- Rich metadata (enrichment) includes: imports, functions, classes, exports, stats (LOC, counts), first doc/comment line, large-file skip marker.
- Hashless hierarchical folder headings: decorative top (root) and second level using equals framing; deeper levels plain with indentation.
- Star highlighting: important/framework entry files (e.g. App.*, index.*, main.*) automatically prefixed with a star symbol.
- Caching: JSON cache keyed by file path + mtime to avoid re‑parsing unchanged files between enrichment runs.
- Config persistence: extension toggle states saved per root for consistent UX across sessions.
- Performance optimizations: directory pruning, binary extension skipping, file size guard, deferred metadata parsing until enrichment.
- GUI (Tkinter): threaded operations, extension toggles with counts, language enrichment toggles (Python / TS-JS / C#-Java), colorization, token estimate, deselect-all types.
- CLI entrypoint: scan rendering and blueprint ingestion via arguments.
- Blueprint ingestion: parse existing blueprint to focus future scans (regex of heading patterns) – adapted for hashless headings.
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

## High-Level Flow (Two-Phase Model)
1. User selects root (GUI) or passes via CLI.
2. Structure Scan (no metadata): hierarchy + extension discovery only.
3. User adjusts: extension checkboxes (visibility), "Deselect All Types" if needed, language enrichment toggles (Python / TS-JS / C#-Java).
4. Enrichment Pass (AI mode only): deep parse limited to selected extensions & enabled languages; populates imports, functions, classes, exports, stats, doc summary.
5. Renderer outputs folder headings, description placeholders, starred files. If enriched, AI metadata lines appear under each file.
6. Token estimate displayed (character_count / 4). User can re-run enrichment after changing toggles or save Markdown.

## GUI Additions (Step 2 Update)
- Buttons: "Scan (Structure)" and "Enrich Context" (second enabled after first pass in AI mode).
- "Deselect All Types" button quickly unchecks every extension.
- Language Enrichment toggles: granular control to include/exclude metadata parsing per language family.
- Token count label: approximate tokens = total characters / 4 after each scan or enrichment.
- Enrichment gating: no 📕 metadata lines appear until the user presses Enrich (reduces initial latency).

## Metadata Lines (AI Mode After Enrichment)
Each enriched file may include (only lines with data are shown; order preserved):
1. 📕 Imports: <list>
2. 📕 Functions: <list>
3. 📕 Classes: <list>
4. 📕 Exports: <list>
5. 📕 Stats: LOC <n> | funcs <f> | classes <c> | exports <e>
6. 📕 Doc: <first docstring / top comment line>
If a file exceeded size guard: 📕 Skipped: large file

## Rich Metadata Extraction Details
- Python: AST for imports, functions, classes; exports via __all__ or top-level defs; docstring first line.
- TS/JS: Regex for imports, functions, classes, exported symbols (`export` statements); first doc comment not yet extracted (future improvement). 
- C#/Java: Regex heuristics for imports (`using`/`import`), function-like signatures, classes, and exported/public identifiers; first block or line comment group as doc summary.
- Stats: simple line count captured only during enrichment (performance optimization).

## Performance Notes
- Initial structure scan skips reading full file contents except to enumerate names; enrichment defers heavy parsing until explicitly requested.
- Large file (>400KB) skip policy unchanged; such files receive only a skip marker.
- Line count calculation deferred to enrichment reduces first-pass time on large trees.

## Future Considerations
- Optional auto-enrich toggle post-structure scan.
- Collapsible metadata sections for very large outputs.
- Additional languages (Go, Rust) via pluggable parser registry.
- More robust doc extraction for TS/JS (JSDoc) and Java (Javadoc multi-line summarization).
- Select-All counterpart to Deselect-All.

## Notes
- Colorization and formatting do not alter underlying output semantics (safe for ingestion by tooling expecting plain text).
- Large binary or oversized source files are skipped from deep parsing to preserve responsiveness.
- The design aims to keep tests minimal but focused on structural guarantees (presence of core markers, star symbol, headings).

