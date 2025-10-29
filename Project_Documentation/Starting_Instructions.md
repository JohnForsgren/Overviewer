
DESCRIPTION: I need a script which goes through an existing code-base and, by running the app in the root folder, it produces a script that clearly shows the file structure of the project (See Example Output below for a suggestion). 

The focus is on the code base itself, not on project dependencies like node_modules, venv (virtual environments in the project root), git, or installations with .NET (bin / obj) or python (__pycache__). 
Those files should simply be ignored, since including them in the output would lead to it being massively cluttered with irrelevant info. This leads to a secondary issue which is to know beforehand which folders should be ignored. The answer would be (1) Focus on simply implementing this for the specific languages used at this time (React Typescript, Python, C# and Java)

Central idea of the script : Give a quick overview of the files in question. 
I don't really have a clear idea of how this should be done - please feel free to expand with ideas from this initial draft. The example below is just the initial draft idea that I have. The idea is that the project should be able to give some more context of the application beyond the initial files. I don't really have any specific idea on this at this time, but some very rough brainstorms would be: 
Include the libraries which are made use of (e.g imports); These would likely be included in the top of the application
Include the specific functions/methods listed in each script. 
Include potential other relevant info. 

I guess that for e.g css and scss, this process can be skipped since I don't see any way in which a script could give a sensible overview of such a file. 


Two different scopes: 
ALSO: There should be a switch for the project purpose: Developer or AI, i.e which the end user of the output file is.   
If the target is Developer, it is more important that it is in a readable/digestable format. 
But if it is for an AI, it can be more verbose: I don't have an exact idea to illustrate what I mean here, but for example, if it is for an AI you could list for each individual file: The names of all functions in the code-file as well as all imports. This could give the AI useful context, but would be frustrating for a developer to read. 

The General FLOW of the application

The application should be managed through a frontend interface (e.g in pythong) from which the application is defined. Broadly speaking, i am thinking: 

1. DOCUMENT SETUP: The first step is to simply include the "stage", i.e a document is defined that contains all of the interesting files in the project. A brainstorm suggestion here is that we open the frontend application from which we select the path to a root folder of a Repo (e.g a react application). The program then shows us a breakdown of the current project in the same style as the blueprint below (but without comments). It excludes already from the start the obviously unnecessary folders/files like Pycache. From this file, the program shows all file types that are registered, and the user can click on a cross/Checkbox to select/unselect them from the output (e.g if the folder has ".bat"-files, this file type can be toggled off if the user wants). This updates the preview of the output file, which the user can then save once satisfied. 
2. FILL IN DATA: The next step is that the user creates the more complete "Information file", whereby the script goes into the documents and extracts relevant info. Here, I don't have a great idea of what to do; this goes back to what i said under "Central idea of the script". It does not have to be super concise, but not too long either. The idea is just that it should contain as much relevant info about the file. 
3. FILL IN DATA THROUGH AI: The third step is for an AI to manually go into the documents and fill in relevant context in them, but this is not done by the script. 

Example Blueprint 2: 
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
* App.tsx 🧠 The main file; creates the frontend interface by calling other modules (Components) <-- EXAMPLE COMMENT. Important files will have manual comments listed like this. This is added by the uyse




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




# Additional functionality 

Pulling up a custom interface for the files
Basically, the general idea here is that I as the user of the app should be able to provide my own custom file that is organized as per a standard for the app (e.g as the example below). This structure will then tell the program to go through these exact files and populate them with information as per the previous norms.

The first thing that should be implemented in this regard is a clear standard for how the folder structure is represented in the markdown file. I.e there must be a good standard so that this file 

Notes to self / Points to consider for initial development (SPA & PDF repos)

Sorting out the unnecessary files from the database
- I must first find a way to really sort out the necessary files in the code base. There are multiple less interesting files that shouldn't be included, so a first central task is to sort this out within the project. STARTING POINT: In general a likely GREAT idea for this is to simply have a script that prints out the folder structure for all files (i.e all files that are not obviously irrelevant, e.g pycache etc as described above), and then we can sort out the less relevant files after that. 


Note-to-self: HIGH PRIO SUGGESTION:
Use Claude/COPILOT to simply go through the files in question and populate them with PROPOSALS for what the file purpose is. I.e: 
1. Identify the relevant files: 
2. Create the map chart as pre the previous example
3. Prompt Claude/Copilot with something like "I need you to use this structure in order to go through the files in this script, read them, and summarize them". 
