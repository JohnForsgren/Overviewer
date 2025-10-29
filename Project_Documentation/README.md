# Overviewer App

Overviewer generates structured Markdown blueprints of a codebase, focusing on meaningful source files (TS/JS, Python, C#, Java) while ignoring dependency/build and cache artifacts. It supports two verbosity modes (Developer vs AI) and provides both a GUI and CLI.

> For deeper architecture, internal data model, and parsing flow see `Project_Documentation/Project_Documentation.md`.

## Goal
Give a rapid, human or AI digestible snapshot of a repository: hierarchy, important entry points, and (optionally) imported modules and defined functions per file.

## Features
- GUI to select root folder, toggle file types, choose target (Developer or AI) verbosity, preview & save.
- Walks directory tree excluding common noise (`node_modules`, `__pycache__`, build output, VCS metadata).
- Extracts lightweight metadata: imports & function/method names (omitted in Developer mode, included in AI mode).
- Markdown rendering with folder headings (📁), description placeholders (📄), file lists, and annotation symbols (⭐️ 📕 🤖 🧠).
- Auto-starring of obvious entry files (e.g., `App.tsx`, `index.tsx`, `main.py`, `Program.cs`).
- Blueprint ingestion: parse existing overview markdown and rescan limited subset.
- CLI for scripting / automation.

## Symbols
| Symbol | Meaning |
| ------ | ------- |
| 📁 | Folder heading |
| 📄 | Description placeholder under a folder |
| ⭐️ | Important / starred file (auto or manual) |
| 📕 | General info added by script (imports/functions) |
| 🤖 | Info added by an external AI agent (future manual enrichment) |
| 🧠 | Manually curated insight by a human or smart agent |

## Installation
```
pip install -r requirements.txt
```

## Quick Start (CLI)
Generate an AI-oriented verbose blueprint:
```
python -m overviewer scan --root C:/path/to/project --mode ai --output blueprint.md
```
Developer concise blueprint:
```
python -m overviewer scan --root C:/path/to/project --mode developer --output blueprint.md
```
Launch GUI:
```
python -m overviewer gui
```

## GUI Flow
1. Browse to repository root.
2. Toggle file type checkboxes (extensions) to include/exclude.
3. Choose mode (Developer / AI).
4. Click Scan to preview markdown.
5. Save Markdown.

## Modes
| Mode | Target | Includes | Intent |
|------|--------|----------|--------|
| developer | Human reader | Hierarchy + ⭐ entry files | Fast onboarding skim |
| ai | LLM / tooling | + Imports & function names (≤25 each) | Richer semantic context |

Switch mode via CLI `--mode` flag or GUI dropdown.

### Example (Truncated)
```
======= 📁 my-app/ =======
📄 Description:
⭐️ App.tsx
index.tsx
📁 src/
📄 Description:
	components/
	📄 Description:
	Button.tsx
```
AI mode would additionally insert lines like:
```
	📕 Imports: react, react-dom
	📕 Functions: Button
```

## Blueprint Ingestion
If you have an existing blueprint file:
```
python -m overviewer ingest-blueprint --root C:/repo --blueprint existing.md --mode ai --output refreshed.md
```
The scan will be narrowed to folders found in the existing blueprint headings.

## Extensibility Ideas (Summary)
- Custom ignore patterns via config file
- Persist manual stars & annotations
- Additional language parsers / deeper AST metadata
- Export variants (JSON outline, Graphviz)
- Incremental & parallel parsing for very large repos

Full discussion lives in the architecture document.

## Limitations
- C#/Java parsing is heuristic (regex-based), may miss edge cases
- Imports/function extraction intentionally shallow (performance-first)
- GUI does not yet allow inline editing of annotations
- Large files (> ~400KB) skip metadata parsing silently
- Manual annotations (🤖 / 🧠) are not yet persisted across rescans

## Testing
Run unit tests:
```
python -m pytest -q
```

## Contributing
Suggestions & PRs welcome. Keep additions modular: add new language parsers under `scanner.py`.

## License
MIT (add actual license file if distributing).
