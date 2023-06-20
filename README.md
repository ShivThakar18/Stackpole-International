# Stackpole-International
This repository contains all the programming-related projects I worked on during my co-op term at Stackpole International. 

## Audit Follow-Up Program
This program is designed to work alongside the Daily Quality Audit Database and Dashboards. When an audit is completed and an entry includes a follow-up action and person, this program takes this data and writes it to a pre-formatted Excel Sheet to be viewed and edited by the Quality Department.

## CMM Programs
- Clutch Hub Copier
- Duramax Excel Exports
- Gear From Printer
- Gleason

### Clutch Hub Copier
This project is designed to pick up new reports for the Clutch Hub's Flatness Scans and deliver them to the Quality Supervisor's Network Folder. 

### Duramax Excel Exports
This program is designed to read a specific output file from the Duramax CMM and converts it to a readable Excel Spreadsheet. Once a new chr.txt file is found for a specific part, it is opened and data is extracted from each line which is stated within a part- and process-specific template. Each dimension in the template notes the FUNCTION and ARGUMENTS. The function tells the program which mathematical process to use on the arguments. The arguments are which lines the characteristic appears in the chr.txt file. This is then simplified to an Excel sheet that helps the CMM Programmer and Operator read the data and determine if the part is GOOD or BAD. 

### Gear Form Printer
This project is designed to pick up new Gear Form Exports for the Duramax CMM and automatically print them to the CMM Room printer for the CMM Programmer and Operator. 

### Gleason
This project was designed to run alongside the Gleason CMM Machine at Stackpole PMDA. A program on Gleason creates a CSV file that will be modified using this Python script. The Python script reads the latest CSV file and extracts specific rows and writes them into a new Excel file. The Excel file is formatted and printed using the default Windows printer. The program on the Gleason computer automatically archives this CSV once the Excel file is printed. 


## Enterprise Report Scheduler - Stackpole Quality Terminal 
This project was designed to allow the Quality Manager and Quality Engineers to navigate ERS Reports more efficiently. This Python program uses the Tkinter Python library to create a user interface where QEs can review the history of the ERS Scheduler. The main purpose is to be able to easily search for specific parts and view their Cpk Reports, Raw Data Export, and Histogram (if applicable). 

<p align="center">
  <img src ="https://user-images.githubusercontent.com/94186009/213518166-5ea449bc-cd0b-4207-885a-7dcccb6dcb7f.png" alt="ERS Terminal UI"/>
</p>

## Equator File Transfer
This is a simple program designed to move files from different drives to the QC-CALC Communication Folder.

## Sediment Tests
This is a program designed to read a PDF Sediment Test and extract specific values (depending on the part group). This program looks for new Sediment Tests and extracts data and sends it to Node-Red Flow. This Node-Red Flow uses the data to check the specifications if they fail an email notification will be sent to the specified Quality Engineer, Quality Manager, and Metallurgical Lab Supervisor. The data is also saved to a database and will be able to use SQL Queries to visualize the data on a Grafana Dashboard.

