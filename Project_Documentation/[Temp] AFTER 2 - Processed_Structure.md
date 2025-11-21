# ======= 📁 data-integration-platform/ =======
⭐⭐ App.tsx 🤖 Huvudfilen som kopplar ihop vyer, dataflöde och startlogik.
⭐ index.tsx 🤖 Startpunkt som monterar appen i sidan.
README.md
# === 📁 build/ ===
app.bundle.js

# === 📁 dist/ ===
index.html

# === 📁 src/ ===
📁 src/features/
    src/features/dataImport/ 🤖 Importerar rådata och normaliserar format.
        importEngine.ts
        parser.ts
        sourceMapping.ts 
    📁 src/features/analytics/ 🤖 Skapar rapporter och visualiserar KPI:er.
        charts.tsx
        reportService.ts
        staleChart.old.tsx
    📁 src/features/ui/ 🤖 Grundläggande visuella komponenter.
        NavBar.tsx
        Footer.tsx
        Modal.tsx

# === 📁 docs/ ===
🤖 Dokumentation & historik. 
⭐ Architecture_v2_draft.md
Architecture_v1.md
ProcessNotes.old.md
run.log
scratch.json