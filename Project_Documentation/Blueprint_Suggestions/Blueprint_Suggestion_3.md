This blueprint outlines the structure for the project overview file.

*   **Folder Representation**: Each folder is represented by a Markdown heading (`#`, `##`, etc.). The heading is prefixed with the `📁` symbol and includes the full path ending with a slash.
*   **Comment Representation**: A placeholder for a descriptive comment, labeled "Description:", is placed directly under each folder heading and is prefixed with the `📄` symbol.
*   **File Representation**: Files are listed as plain text under their respective folder sections. They do not have any special prefixes.



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

    📁 features/breadcrumbs/
    📄 Description:

    types.ts
    useBreadcrumbs.ts
    
        📁 features/breadcrumbs/components/
        📄 Description:

        breadcrumbs.tsx

    📁 features/changeManual/
    📄 Description:

    [...]
