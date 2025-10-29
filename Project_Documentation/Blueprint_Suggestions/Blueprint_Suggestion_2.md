This blueprint outlines the structure for the project overview file.

*   **Folder Representation**: Each folder is represented by a Markdown heading (`#`, `##`, etc.). The heading is prefixed with the `📁` symbol and includes the full path ending with a slash.
*   **Comment Representation**: A placeholder for a descriptive comment, labeled "Description:", is placed directly under each folder heading and is prefixed with the `📄` symbol.
*   **File Representation**: Files are listed as plain text under their respective folder sections. They do not have any special prefixes.


# Additional comments/Symbols that are added through the script: For each component, there should be additional info added.

* Star (⭐️): Added by user for important documents. The script can also automatically add stars for obviously important files like App.tsx
* General info (📕): Refers to general info that has been added through the overview script itself. This would primarily be used in the AI-version, i.e the output script that it designed to be used by AI. 
* Robot (🤖) Refers to info added by an AI who manually goes through the file and makes an assumption. 
* Brain (🧠): Refers to manually added info by a "smart" agent (human or AI), i.e not the script. 

Examples: 
* App.tsx 🧠 The main file; creates the frontend interface by calling other modules (Components) <-- EXAMPLE COMMENT. Important files will have manual comments listed like this. This is added by the user.  


# --- THE BLUEPRINT --- 
# 📁 src/
📄 Description:

App.test.tsx
App.tsx
index.css
index.tsx
types.ts

# 📁 components/
📄 Description:

Button.tsx
Checkmark.tsx
Page.tsx

# 📁 features/
📄 Description:

## 📁 features/breadcrumbs/
📄 Description:

types.ts
useBreadcrumbs.ts

### 📁 features/breadcrumbs/components/
📄 Description:

breadcrumbs.tsx

## 📁 features/changeManual/
📄 Description:

[...]
