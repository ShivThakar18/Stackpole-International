# Enterprise Report Schedular - Stackpole Quality Terminal
This project was designed to allow the Quality Manager and Quality Engineers to navigate ERS Reports more efficiently. This Python program uses the TKinter Python library to create a user interface where QEs can review the history of the ERS Scheduler. The main purpose is to be able to easily search for specific parts and view their Cpk Reports, Raw Data Export, and Histogram (if applicable). 

<p align="center">
  <img src ="https://user-images.githubusercontent.com/94186009/213518166-5ea449bc-cd0b-4207-885a-7dcccb6dcb7f.png" alt="ERS Terminal UI"/>
</p>

## Libraries Used
- os: path, stat, startfile, remove
- glob: glob
- tkinter
- tkinter.messagebox
- datetime: datetime
- subprocess
- functools: partial
- shutil: copy
  
## How It Works and Terminal Walkthrough
Once the user has opened the application using the executable file, they will see the main menu where they will be able to conduct different actions. 

"Report Search" - allows the user to search any part name/number and open the last Raw Data Export, last CpK Report, last Histogram, or open the Part Folder with all reports. 

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/ae430a31-20a8-4b66-b508-08ffe47aa00f" alt="Report Search"/>
</p>

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/9fcd1676-c8ca-40f4-9c67-b0392645db5e" alt="Report Search"/>
</p>

"View Report History" - show a list of all the most recent reports (dependent on part or overall)

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/93059b00-4e26-4656-8b4a-df1ed670dc0e" alt="Report Search"/>
</p>

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/852f8026-dbea-46f7-a27b-293b330cc18e" alt="Report Search"/>
</p>

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/643874d2-a4a1-4935-af44-926cf2114fff" alt="Report Search"/>
</p>

"Open Schedule" - opens an Excel spreadsheet that summarizes each part and their scheduled time of export

"Settings" - allows the user to change the maximum number for the history

<p align="center">
  <img src ="https://github.com/ShivThakar18/Stackpole-International/assets/94186009/6a902a54-c699-478e-bc94-4e71b6fe2402" alt="Report Search"/>
</p>

## Setup
Simple setup procedure. 
### Python Libraries
- os: mkdir, rmdir, path, rename, remove
- shutil: move
- glob: glob
- zipfile: zipfile
- winshell
- win32com.client
  
### Setup Execution
I have set up another executable file that will complete all the setup automatically.

Once the executable file is initialized, the program extracts a zip folder with the latest update of the Terminal and automatically copies all the files needed (removes files from previous versions), and creates a shortcut on your desktop. 

If there is a new version available, the user just needs to start the executable file and will automatically be updated to the latest version.
