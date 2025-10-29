# Overviewer Project Documentation (AI Onboarding Snapshot)

Purpose of this document: Rapidly orient an AI (or a human skimming fast) to the current feature set, architecture touch‑points, and parsing/enrichment logic. It is intentionally concise and NOT a user guide or exhaustive operational manual. It describes what exists (and key design intentions) so follow‑up reasoning or code generation can proceed with minimal clarification.

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
- GUI (Tkinter): threaded operations, extension toggles with counts, per‑extension enrich checkboxes (only shown for supported enrichment file types), colorization, token estimate, select/deselect utilities.
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
3. User adjusts: extension checkboxes (visibility). Utilities: Select All, Deselect All, Select Only Supported Code Files. Per‑extension "Enrich" toggles determine which types receive deep parsing.
4. Enrichment Pass (AI mode only): deep parse limited to selected extensions & only those with Enrich enabled; populates imports, functions, classes, exports, stats, doc summary.
5. Renderer outputs folder headings, description placeholders, starred files. If enriched, AI metadata lines appear under each file.
6. Token estimate displayed (character_count / 4). User can re-run enrichment after changing toggles or save Markdown.

## GUI Elements (Current)
- Buttons: "Scan (Structure)", "Enrich Context" (enabled after first structure pass in AI mode), "Save Markdown".
- Extension area: dynamically discovered extensions each with an Include checkbox and (if supported) an Enrich checkbox.
- Utility buttons: Select All Types, Deselect All Types, Select Only Supported Code Files.
- Token count label: approximate tokens = characters / 4.
- Colorize toggle for extension‑based coloring of file lines.
- Enrichment gating: no 📕 metadata lines until explicit Enrich.

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
Supported enrichment extensions now include: `.py .ts .tsx .js .jsx .cs .java .sh .xsl .xml .dita .ditamap .scss .css`

- Python (.py): AST for imports, functions, classes; exports via `__all__` or top-level defs; first docstring line.
- TypeScript / JavaScript (.ts .tsx .js .jsx): Regex for imports, functions, classes, exported symbols; (doc extraction TBD).
- C# / Java (.cs .java): Regex imports, function-like signatures, classes, public identifiers; first block or line comment group as doc summary.
- Shell (.sh): Shebang + sourced scripts treated as imports; function definitions via `name() {`; first non-shebang comment line as doc summary; star heuristic for filenames containing deploy/start/run.
- XSL (.xsl): `<xsl:import|include>` as imports; named + match templates aggregated as functions; stylesheet tag snippet as doc summary.
- XML (.xml): Root element + namespace declarations (treated as imports); distinct tag count summarized in doc line.
- DITA (.dita .ditamap): Root element; keyrefs (imports); href count; summary of root + keyref/href counts.
- SCSS (.scss): `@use/@import` targets as imports; mixins as functions; counts for vars/mixins/selectors in doc summary.
- CSS (.css): Count of selectors and media queries in doc summary.
- Stats: line count + aggregate counts (funcs/classes/exports) only computed during enrichment.

## Performance Notes
- Initial structure scan avoids parsing content bodies; enrichment defers heavy parsing until requested.
- Large file (>400KB) skip policy unchanged; skipped files get a marker (no expensive parsing).
- Line counts only during enrichment.
- Regex extraction additions (shell/xsl/xml/dita/scss/css) are lightweight; each runs only on explicitly selected, enriched extensions.

## Future Considerations
- Persist per-extension Enrich selections across sessions.
- Optional auto-enrich after structure scan.
- Collapsible metadata regions for large outputs.
- Deeper doc extraction: JSDoc/Javadoc, XML schema awareness, XSL template mode summarization.
- Plugin registry for new parsers (Go, Rust, PHP, etc.).
- Heuristic quality scoring (e.g., functions per LOC) for future analytics.

## Notes
- This file is intentionally concise and factual; omit marketing prose.
- Colorization & formatting do not alter semantic content (safe for downstream ingestion).
- Oversized or binary files are skipped for performance; logic is deterministic given inputs + toggles.
- Tests (expanding) should assert structural invariants rather than replicate parser internals.

