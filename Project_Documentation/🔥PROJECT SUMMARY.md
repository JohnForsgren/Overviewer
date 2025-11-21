



PROMPT TO AI: I have this personal document where i write with my own words my vision of the project; dont' change this too much or add a bunch of superflurous information. I just need some guidance for how this can be expanded upon for more contex. 
(This is a brief summary; i don't want to be to long here since this sort of thing is likely already written in more detail elsewhere, but i cant find it atm)


# PROJECT SUMMARY : How to manage the Overviewer app and its output folder structure. 

The overall vision with the project is to create one or a few files which give a clear project overview; it can target either a human user or AI, or both. The purpose is to enable a user to quickly with a single document get a good understanding of the whole code base by having a clear file that does things like: 

1. Lists the project folders in a clear and readable way [I have put together a good blueprint for this, listed below. ]
2. Consisely summarizes files. By "Consise" i do not necessarily mean that the descriptions have to be very short, but that they are optimized to give as much relevant info while minimizing superflorous text. 
3. Optionally, inside the overviewer script, the script has added general metadata tagged with the symbol "📕" (see below)

Much of the project purpose relates to the use of coding agents (e.g Github Copilot or Google's Gemini CLI). This means that it becomes relevant both for human users and AI. 

TARGET: HUMAN USER:
- The solution enables human users to get more context about the code base so that they can more easily grasp it. The document can be used by a developer to add relevant comments for both himself and the AI. This is especially useful for apps where AI coding agents write much of the code. This file helps the user to be up to date. 

TARGET AI:
- The AI can use the document at the start of a chat to quickly become up-to-date on the projhect, without having to manually read a bunch of files. It also reduces the likelyhood that the AI implements soltuions that already exists, or solutions in the wrong places. 
- A general idea I have been trying to implement in the project is that an AI should be able to write scripts that go into individual files, check them for general useful content such as imported libraries and function names, and report them as general "metadata" in a large-file (marked by the symbol "📕"). This would enable the AI to quickly have an understanding of the project structure. This has been done in the Overviewer project, but the same structure can also be used without the overviewer script, by the AI simply generating the files. 

GENERAL GUIDES for how the AI should manage these documents: 
- A thing to AVOID in this regard (For an AI who is supporting the project): Do not add a bunch of long comments (especially not unless the user has asked for it) to the file. Potentially, there could be two DIFFERENT overview-files of the project where there is a separate one that is dedicated for an AI, where it is possible to be more verbose, since human-readibility isn't critical.
- Another thing to remember is that AI agents can read the content of individual files, so the overview should just briefly summarize them, Notably: 
    - Not all files even need a description; many files can be simply understood what they do based on ther name and the folder they are placed in. 
    - Not much comment is needed beyond a brief description of the file, UNLESS there is some important aspect to consider, e.g if a less than ideal solution has been implemented that should be adressed later, or if a necessary "workaround" or similar is created which is infeasible to change, this might be listed as a warning. 
    - Notably, as has been achieved by the Overviewer app, many files are not listed at all. It is just the files that relate to development that are important. Especially Libraries (e.g venv installations, __pycache__ etc ) are completely irrelevant. Many other files can potentially also be irelevant. For details on this: see the Overviewer project file "filters.py"  


<<<<<<<<<<< TO ADD HERE: Ask the AI : Is there i have missed based on this, based on what is written in the other files in the project documentation. Also, are there any incomplete sentences or inaccurate/misleading statements? 


## Emojis for clarity
In order to make it more readable, especially for humans, some emojis are used: 
This should be the main source of truth for the emojis that are used. 
◇ = Used to denote a individual files 
📁 = folder
📄 = description (Typically of a folder)
🤖 = AI-generated comment. AI:s should always mark their comments with this emoji, so that it is clear what has been written by AI (Consider having a human user verify it later)
🧠 = Human generated comment 
❗ = Issue to adress at some point 
⚠️ = Warning; Important to remember and/or adress soon. 
⭐️ = important file. Up to 3 stars can be used for a file folder, to express that certain elements are especially important. 
📕 = Only used for elements generated by the "Overviewer" script, where several scripts (i.e not an ai) go into the code and 
💥 = Question 

## Headings / Levels. 
The headings are made in this particular way to creat clear readibility. 
The headings are used to break down the folder structure; each heading is used 

Level 1: # ======= 📁 pdf-refactoring/ =======
Level 2: # === 📁 base/ ===
Level 3: ## 📁 base/css/     NOTE: Starting here at level 3, there are indents instead of "#"-markings, as per the example below. 
Level 4: 📁 base/scss/modules/



# ======================== THE BLUEPRINT ======================== 

Here is an example of the current blueprint (the latest version as of 2025-11-21), condensed with lots of files removed (this is not meant to show the actual repo, just to make an example of how it might look in practice )

# ======= 📁 pdf-refactoring/ =======
◇.index.properties
◇build.sh 🧠 Builds the entire zip-file that is the whole application that we can directly push to TPS. This can be used when we need to push to production, or to debug. This Zip-file includes the necessary content to run the pdf-refactoring application, such as the folders: assets, base, lib, module. The application can then run in TPS, where users of TPS can generate their PDF:s 
◇compose_input.xml -> 🧠 
    * compose_input.xml is used in the publish script along with compose_input.xml: base/xsl/postprocess/VariableAppender.xsl
    * 💥 QUESTION to Joseph: Relating to the keyrefvalues.dita: This file must come from TPS, and is placed on the root level, just like all other dita-files. But Mikael has never encountered this file before, so is still used? If this is not used, we could likely remove the VariableAppender, since that file is dependant on the keyrefvalues.dita. 

◇compose_output.xml -> ❗ Likely depricated and not used at all. Should be deleted if we can confirm this.   
◇publish.sh - 🧠 Not relevant for local testing. 
◇⭐️⭐️publish_test.sh - 🧠 This is the main file we use when testing locally (i.e we do not use the other "publish[...].sh" files)
    🧠 Essentially the whole application takes place from this file. It can be summarized very breifly as: 
    1. We take in DITA and DitaMap files from TPS (TechPub Studio) that make up a whole or a part of a Turbine manual for Siemens, which is intended to be the output of this entire repo
    2. publish_test.sh processes these input files, referencing the various code files in this project.  
    3. At the end of this, we have our desired output pdf. 
    🧠 Saxon 9, which is used repeatedly in the publish.sh-scripts, is the XSLT 2.0 processor; This is the engine that executes our stylesheets to transform XML into our other XML/HTML outputs. 

◇⭐️publishConfiguration.xml - 🧠 This is an important file since it relates to the metadata settings / configuration for the document which is set in TPS: Here we set the Publishing tool, and select things like: Language, Page Format, Orientation, and if it should contain Coversheet, TOC (Table of Contents), Indexterms and Reference List. 

# === 📁 base/ ===
📄 Description: 🧠 The base folder is the main one that we are working with.

## 📁 base/css/
    📄 Description:
    ◇⭐️ print-base.css  🧠 This is the css that is used by the final output html document that the PDF-repo aims to create. It is this html+css that is sent to antennahouse to create the final output pdf. The print-base.css is created through base/scss/. 
        
    ◇print-base.css.map - 
    ◇print-compare.css - 
    ◇web-base.css - 🧠 The web-functionality is currently not used by our team. There might be an argument to delete them to refactor our old legacy code. 
    ◇web-base.css.map
    ◇web-ootb.css
    ◇web-ootb.css.map

## 📁 base/resource/
    📄 Description:
    ◇strings.xml -> Contains translations. Consider merging with translations.xml? 
    ◇system-msg.xml

## 📁 base/scss/
    📄 Description: 
        🧠 FOLDER PURPOSE: The scss folder is used to create the print-base.css file.  
        🧠 Sassy CSS allows us to break down CSS into smaller components, use variables, and use css in a more modularized way. 
    ◇⭐️ print-base.scss 🧠 This goes through all ".scss"-files in the folder "partial" and determines which order they are processed.
         🧠 The command "npm run sass_autocompile_base" is used to autocompile the scss to the css folder. 
    📁 base/scss/partial/
        📄 Description:
    ◇_shame.scss - 🤖 Appears to be a “dumping ground” / last‑resort overrides files. The file has multiiple "red flags", discussed in the document "Details on specific files.md". Examples include multiple `!important`, deep descendant chains (e.g `#publication .toc ul ul li a span`) and "ID + many classes purely for specificity". It is relatively short though, so it shouldn't cause too much problems in its current state.
    ◇_table.scss
