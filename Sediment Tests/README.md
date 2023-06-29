# Sediment Tests Database
This project was meant to update a pre-existing program, Jomesa 3.2. During the development of Jomesa 4.0 which was supposed to add new part compatibility, a new idea was thought of. Jomesa 5.0 will add many new features to the program such as: 

- Inheritance (many Python files and functions) 
- Grafana and SQL Integration
- Litmus Edge (Node-Red) Integration
- Simplify Program
  - Remove Spec Validation (will be done through LE)

## Python 
There are a number of Python files used in this project: 
- Main.py - calls functions from other PyFiles
- Settings.py - holds file paths and folder locations that are globally used on all files
- Pictures.py - saved pages in a new PDF that include pictures from the original report when a new file is added to the folder
- One File per Part Group (ZF.py, 10R140.py, GME.py) - searches for files in the part group folder and parses data from pdf reports
  
### Main 
Imported The following functions: 
- Jomesa5_10R140.py: search10R140 , get10R140Data
- Jomesa5_ZF.py: searchZF , getZFData
- Jomesa5_Pictures.py - extractPictures
- Jomesa5_Settings - ORIG_DIR (string)
  
Using an infinite loop, the program checks each Part Group by calling the specified function from their PyFile (e.g. Jomesa5_10R140.py - search10R140, Jomesa5_ZF.py - searchZF, etc.) and adds the returned list to a list using extend. The function iterates through the files in the list and uses the 'get' function from each Part Group File depending on if the group is specified in the file path. At each loop, the main function checks if pictures need to be extracted by calling extractPictures() from Jomesa5_Pictures.py.

### Part Group Files 
- Jomesa5_10R140.py
- Jomesa5_ZF.py

These files contain specific 'search' and 'get' functions dependent on the group because the information that must be extracted from the Sediment Test is different.

### Pictures 
When a file with PIC_DIR+"**\\*_fullreport.pdf" appears in the pictures directory (this happens when Node-Red moves a pdf into this folder when Specs have been validated). Depending on the part group, certain pages are extracted and saved into the PIC_DIR.

## Jomesa 5 JSON (Node-Red)
When a new data file (created by Python) and a copy of the report arrives in the LE_DIR. Node-Red picks up the text file and parses the file with all the data and saves it to flow variables. Once saved, the specs are checked depending on the part and returns the passed and failed specs. The flow will send the data to a SQL server and can be viewed on Grafana. If failed, an email notification is sent out to the Quality Manager and Quality Engineer.

## Grafana Dashboards
There are two visualization dashboards being used. The first is specifically used for Ford Sediment Tests. The second is used for all other parts. 

![image](https://github.com/ShivThakar18/Stackpole-International/assets/94186009/8f16136d-a30b-4e5e-9f72-be8cd1d31f16)

![image](https://github.com/ShivThakar18/Stackpole-International/assets/94186009/4a9fff4b-f56a-49cd-981c-2c7884b53505)

