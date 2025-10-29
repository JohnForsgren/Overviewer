


== Small additions ==
- There should be in addition to "Deselectt all Types" a "Select all types" button. 




== Ensuring Maximum quality of the output == 
The important next step is to ensure that the OPTIMAL LOGIC is used for the RIGHT LANGUAGES. This concerns our PDF and SPA applications. 

3 steps: 
    1. Identify the critical languages to have logic for 
    2. Ensuring we have all of these languages implemented, focusing on the more important languages 
    3. Testing the existing results against some actual existing files; I.e: How does the output compare against the actual file content, and (2) Is there any area of improvement we can make? 

Identifying the central languages here: This is easily done since we can base it on the existing FIle Types list: 

SPA APPLICATION: 
    18 ts files and 43 tsx files. 

    .css -> Only 3 files, not sure if they are used.  

    .sh -> Has only 2 files, HOWEVER, these are critical, so it might be sensibel to have some logic for bash files. Also, bash files should PERHAPS be marked with stars

    The other files are likely not critical at this time. 

PDF application:
    * Xsl files are a critical part of this app
    * xml files 
    * Notably: It has .dita and .ditamap. 
    * Scss files are common here, though it might be tricky since there are no imports/exports here. Additionally, listing existing classes might be misleading since the document might be changed. Though, it could perhaps be sensible to look for some sort of pattern and concisely report the pattern, such as if a particular name or term occurs many times in the same file. 


SPA LOCAL SERVER: 
    This is less important and can be handled later. I guess it is mainly just the java files that matter here. 




=== AFTER THE CODE EDITS HAVE BEEN MADE ===

Send the inpuit chat to a new AI and ask it to judge the current quality of the most important filfes 


Send the inpuit chat to a new AI and ask it to judge the current quality oif the current output based on the following: 
1. The input documentation / project documentation
2. A current output of the overviewer-app (i.e the whole folder structure with associated info)
3. A selection of examples of files from each of the mainfile types (.tsx, .scss, .xsl, etc) -> THis is placed in the UAT Testing Folder


Then ask for additional ideas of what can be done to provide more context 


    === UPDATE REGARDING THE UAT TESTING === 

    TODO NOW:  <<<<<<<<<<<<<<< CONTINUE HERE 
    - Populate the UAT with example files and test. 
    <<<< ONLY THE TYPSCRIPT REMAINS 


=== ADDITIONALLY:: Implement the developer setting ===
As mentioned in the Starting_Instructions, the Developer setting is intended to have info digestible for a developer. I don't have a clear idea yet on what might be included here. 
 
