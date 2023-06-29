# Daily Quality Audits
This project was used to digitize the procedure of conducting Daily Shift Reports. 

## Entry Dashboard
The Daily Quality Audit.JSON file is the first part of the program. This was a designed NodeRed Flow that allowed the user to input different aspects of their audit such as Specific Requests, Critical Calls, and Machines in Bypass. The dashboard uses many UI and Function nodes to create a user-friendly interface. This program also has SQL Integration that feeds all the entries in the audit to a SQL Server and can be viewed in Grafana 8.1. 
![image](https://github.com/ShivThakar18/Stackpole-International/assets/94186009/b797f7ea-8381-44ac-8116-89f3eab39b48)

## Grafana Dashboard - Main Developer (Principal Engineer @ Stackpole Ancaster - Jack C. Fung)
This dashboard was created by Principal Engineer at Stackpole Ancaster. I was new to SQL at the time so I only helped to add some of the panels such as the pie charts. Therefore, the code is not included in this repo.

![image](https://github.com/ShivThakar18/Stackpole-International/assets/94186009/3928f239-a241-426a-a073-0f4ce2cc69ae)

## Follow-Up Actions List
The last component of this project is the Follow-Up Actions list. This is created using a Python program that extracts the FinalDataObject from the Entry Dashboard when a follow-up action was entered. The Node Red Flow automatically writes the Object to a file. The Python program reads the file every day at the end of each shift (7 am, 3 pm, 11 pm), parses the DataObject string, and writes the information to a preformatted Excel file

![image](https://github.com/ShivThakar18/Stackpole-International/assets/94186009/48a60153-99eb-42e1-9b70-d354a1682c1e)
