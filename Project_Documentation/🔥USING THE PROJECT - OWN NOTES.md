


This file is a personal file where i describe my thoughts around the project. The project itself is clearly documented in the other files (readme, Project DOcumentation & Original_Instructions)

The four main steps 


## 1. Setting up the initial documentation
* The app is started, you select the targeted root folder, and generate the initial overview file - deselecting file types thare are not interesting. 

* Unimportant files for the respective repos: 

    * SPA: 
        * .jar files -> Contains no readable code
        * .svg files -> Skip
    * 

## 2. The "Smart context" is added (Based on the completed file in step 1) 
* The current app functionality for this should essentially be fully complete at this point. 

## 3. Context is added by a HUMAN AND an AI 
### 3.1 Human Addon

<<<<<<<<<<<< CONTINUE HERE:  🔥🔥🔥🔥🔥🔥🔥🔥🔥 
* Since i already have existing comments on the current project -> Set up the initial document from step 2 and integrate my own comments. 

* ALSO NOTE: Remove unecessary folders before adding own documentation. 

* ALSO TODO: Add a comment at the top of the document, explaining the document purpose (see below)  

DOCUMENT PURPOSE: 
- The prupose of this document is to give an AI (E.g Copilot) a clear overview of the current repository, without having to send in every file into the model directly. 
- The AI model is encouraged to use this document during development, so that for instance (1) There is an understanding of existing features so that new features are not "reinventing the wheel" [implementing already existing features] or placing the code at the wrong place. 

### 3.2 AI Addon
Here, the idea is that an AI is prompted to manually go into certain files and add relevant content to them. 
For this to work, there must be a PROMPT that guides the AI for which files to go in and check. 

<<<<< NEXT STEP: This is the next stop to continue. Make a prompt here for the relevant documents. 


## 4. Making later updates to the project (if the code-base is changed)

This was discussed in the main doc, and it was concluded that it is most likely best to simply have an AI do this manually INSTEAD of having it existing in the code. 

The original comment was: 
            "Additional very useful (but somewhat risky) feature: Extract the AI- and User provided comments. 
            Ideally, it would be nice if the code could extract the specific AI added comments 🤖 and human comments 🧠, so that these are saved. There is a clear risk in this process as the program might mix up files. Also, it will be tricky to manage if the files are moved or renamed (so i guess this functionality perhaps can be skipped since it is too complex to implement in a single app like this). But what i am envisioning is this: 
            1. The user saves AI-generated comments 🤖 and human generated comments 🧠 in a file. 
            2. The program then extracts the files according to the rules.
            This one seems a bit tricky since a user will be modifying the existing document, meaning it won't always necessarily have a consistent format. <<<<CONCLUSION HERE>>>>: Most likely, this thing should simply be edited through an AI, not the script. 
            3. The current file is then provided with only the specific comments provided
            I.e: comments with 📕 are not included, but 📄, 🤖 and 🧠 are. " 

