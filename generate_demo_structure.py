r"""Generate a demo folder structure that mirrors the 'raw unprocessed' example
for presentation screenshots.

Usage (Windows PowerShell):
    & .venv/Scripts/python.exe generate_demo_structure.py
    # Optional: force rebuild:
    & .venv/Scripts/python.exe generate_demo_structure.py --force

Note: Forward slashes are used above for simplicity; Windows PowerShell accepts them.

Creates a top-level folder 'demo_data_integration_platform' so it
won't clash with any existing real application code.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

DEMO_ROOT_NAME = "demo_data_integration_platform"

# (path -> minimal file content)
FILES: dict[str, str] = {
    # Root level
    f"{DEMO_ROOT_NAME}/README.md": "# Demo Data Integration Platform\n\nPresentation example structure.\n",
    f"{DEMO_ROOT_NAME}/package.json": '{"name": "demo-data-integration-platform", "version": "0.0.0"}\n',
    f"{DEMO_ROOT_NAME}/tsconfig.json": '{"compilerOptions": {"strict": true}}\n',
    f"{DEMO_ROOT_NAME}/ecosystem.config.json": '{"apps": []}\n',
    f"{DEMO_ROOT_NAME}/LICENSE": "MIT\n",
    f"{DEMO_ROOT_NAME}/.env.example": "API_KEY=changeme\n", 
    f"{DEMO_ROOT_NAME}/CHANGELOG.md": "## Changelog\n- Initial demo structure generated.\n",

    # build
    f"{DEMO_ROOT_NAME}/build/app.bundle.js": "// compiled bundle placeholder\n",
    f"{DEMO_ROOT_NAME}/build/build-manifest.json": '{"files": ["app.bundle.js"]}\n',
    f"{DEMO_ROOT_NAME}/build/assets-map.json": '{"css": [], "js": ["app.bundle.js"]}\n',

    # dist
    f"{DEMO_ROOT_NAME}/dist/index.html": "<!DOCTYPE html><html><head><title>Demo</title></head><body><div id='root'></div></body></html>\n",
    f"{DEMO_ROOT_NAME}/dist/favicon.ico": "(binary placeholder)\n",
    f"{DEMO_ROOT_NAME}/dist/robots.txt": "User-agent: *\nDisallow:\n",

    # src root files
    f"{DEMO_ROOT_NAME}/src/App.tsx": "export function App(){ return <div>Demo App</div>; }\n",
    f"{DEMO_ROOT_NAME}/src/index.tsx": "import {App} from './App'; // mount logic placeholder\n",
    f"{DEMO_ROOT_NAME}/src/config.ts": "export const CONFIG = { apiBase: 'https://api.example.test' };\n",
    f"{DEMO_ROOT_NAME}/src/types.d.ts": "declare interface DemoType { id: string }\n",
    f"{DEMO_ROOT_NAME}/src/formatUtils.ts": "export const formatDate = (d: Date)=> d.toISOString();\n",
    f"{DEMO_ROOT_NAME}/src/legacyConnector.ts": "// Legacy connector kept for migration reference\n",
    f"{DEMO_ROOT_NAME}/src/router.tsx": "// Simple route table placeholder\n",
    f"{DEMO_ROOT_NAME}/src/stateStore.ts": "// Basic in-memory state store placeholder\n",

    # features: dataImport
    f"{DEMO_ROOT_NAME}/src/features/dataImport/importEngine.ts": "export function runImport(){ /* ... */ }\n",
    f"{DEMO_ROOT_NAME}/src/features/dataImport/parser.ts": "export function parse(raw: string){ return raw.split('\n'); }\n",
    f"{DEMO_ROOT_NAME}/src/features/dataImport/sourceMapping.ts": "export const MAP = { sourceA: 'internalA' };\n",
    f"{DEMO_ROOT_NAME}/src/features/dataImport/dataValidator.ts": "export function validate(row: any){ return true; }\n",
    f"{DEMO_ROOT_NAME}/src/features/dataImport/transformRules.ts": "export function transform(row: any){ return row; }\n",

    # features: analytics
    f"{DEMO_ROOT_NAME}/src/features/analytics/charts.tsx": "// Chart component placeholder\n",
    f"{DEMO_ROOT_NAME}/src/features/analytics/reportService.ts": "export function buildReport(){ return { kpi: 42 }; }\n",
    f"{DEMO_ROOT_NAME}/src/features/analytics/kpiCalculator.ts": "export function calcKpi(data: any[]){ return data.length; }\n",
    f"{DEMO_ROOT_NAME}/src/features/analytics/trendAnalyzer.ts": "export function analyzeTrend(series: number[]){ return 'up'; }\n",
    f"{DEMO_ROOT_NAME}/src/features/analytics/exportCsv.ts": "export function exportCsv(rows: any[]){ /* ... */ }\n",

    # features: ui
    f"{DEMO_ROOT_NAME}/src/features/ui/NavBar.tsx": "// NavBar component\n",
    f"{DEMO_ROOT_NAME}/src/features/ui/Footer.tsx": "// Footer component\n",
    f"{DEMO_ROOT_NAME}/src/features/ui/Modal.tsx": "// Modal component\n",
    f"{DEMO_ROOT_NAME}/src/features/ui/Button.tsx": "// Button component\n",
    f"{DEMO_ROOT_NAME}/src/features/ui/Sidebar.tsx": "// Sidebar component\n",
    f"{DEMO_ROOT_NAME}/src/features/ui/ThemeProvider.tsx": "// ThemeProvider component\n",

    # docs
    f"{DEMO_ROOT_NAME}/docs/Architecture_v1.md": "# Architecture v1 (baseline)\n",
    f"{DEMO_ROOT_NAME}/docs/Architecture_v2_draft.md": "# Architecture v2 (draft improvements)\n",
    f"{DEMO_ROOT_NAME}/docs/api_reference.md": "# API Reference\n",
    f"{DEMO_ROOT_NAME}/docs/data_dictionary.md": "# Data Dictionary\n",
    f"{DEMO_ROOT_NAME}/docs/deployment_guide.md": "# Deployment Guide\n",
    f"{DEMO_ROOT_NAME}/docs/security_guidelines.md": "# Security Guidelines\n",
    f"{DEMO_ROOT_NAME}/docs/meeting_notes.md": f"# Meeting Notes\nGenerated: {datetime.utcnow():%Y-%m-%d}\n",
    f"{DEMO_ROOT_NAME}/docs/research_notes.md": "# Research Notes\n",
    f"{DEMO_ROOT_NAME}/docs/runtime_metrics.log": "(log placeholder)\n",

    # scripts
    f"{DEMO_ROOT_NAME}/scripts/build.sh": "#!/usr/bin/env bash\necho Building...\n",
    f"{DEMO_ROOT_NAME}/scripts/deploy.sh": "#!/usr/bin/env bash\necho Deploying...\n",
    f"{DEMO_ROOT_NAME}/scripts/seed_data.ts": "// Seeds dev data\n",
    f"{DEMO_ROOT_NAME}/scripts/generate_kpi_report.ts": "// Generates KPI report\n",

    # tests
    f"{DEMO_ROOT_NAME}/tests/App.test.tsx": "test('app loads', ()=>{/* ... */});\n",
    f"{DEMO_ROOT_NAME}/tests/importEngine.test.ts": "test('import runs', ()=>{/* ... */});\n",
    f"{DEMO_ROOT_NAME}/tests/reportService.test.ts": "test('report builds', ()=>{/* ... */});\n",
    f"{DEMO_ROOT_NAME}/tests/charts.visual.test.tsx": "test('charts render', ()=>{/* ... */});\n",
}

TEXT_EXTENSIONS = {'.md', '.json', '.ts', '.tsx', '.sh', '.log', '.d.ts', '.yaml', '.yml', '.env', '.example', '.txt'}


def create_files(force: bool = False) -> None:
    root = Path('.')
    target = root / DEMO_ROOT_NAME
    if force and target.exists():
        shutil.rmtree(target)
    for relative, content in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not force:
            continue  # don't overwrite unless forcing
        mode = 'wb' if path.suffix not in TEXT_EXTENSIONS else 'w'
        if mode == 'wb':
            path.write_bytes(content.encode('utf-8'))
        else:
            path.write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Generate demo folder structure for screenshots.")
    parser.add_argument('--force', action='store_true', help='Force recreation (delete existing folder first).')
    args = parser.parse_args()

    print(f"Using Python interpreter: {sys.executable}")
    create_files(force=args.force)
    print(f"Demo structure created under ./{DEMO_ROOT_NAME}")
    print("You can now take screenshots of the folder tree.")

if __name__ == '__main__':
    main()
