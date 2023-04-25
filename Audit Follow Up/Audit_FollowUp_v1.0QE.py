
# *------------------------------------ Shiv Thakar - Quality Engineering Intern ------------------------------------- #
# *--------------------------------------------- Stackpole International --------------------------------------------- #
# *------------------------------------ Daily Quality Audit Follow Up Application ------------------------------------ #
# *---------------------------------------------- Date: April 4th, 2023 ---------------------------------------------- #
# !------------------------------------------------------------------------------------------------------------------- #
# !                                               Import Python Modules                                                #
# !------------------------------------------------------------------------------------------------------------------- #
from os import path, rename,stat
from glob import glob
from tkinter import *
import tkinter.messagebox
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from shutil import copy, move
from time import sleep
from openpyxl.styles import Alignment
import copy
from os import remove
from datetime import datetime
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                 Define Variables                                                   #
# !------------------------------------------------------------------------------------------------------------------- #
LITMUS_DRIVE = "L:\\ShivDataOutput\\Daily_Quality_Audits\\Follow_Up\\"                      # file source
DATA_FOLDER = "N:\\Quality\\Daily Quality Audits\\"  # file dest
FILE_LOC = DATA_FOLDER + ""
XLSX_FILE = "Audit Follow Up List.xlsx"
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                     Functions                                                      #
# !------------------------------------------------------------------------------------------------------------------- #                                        
# ?------------------------------------------------ Parse and Extract ------------------------------------------------ #
def parseFile(FILE):

    m_file = open(FILE,'r')                                       #
    m_data = m_file.read().splitlines()
    length = len(m_data)
    m_file.close()

    if(stat(FILE).st_size == 0):
        print("File Empty")
        return

    for i in range(len(m_data)):
        m_data[i] = m_data[i][1:-1]
    
    data = []
    temp = []

    for m in m_data:
        temp = m.replace(",\"","|\"")
        temp = temp.split("|")

        i = 0
        for t in temp:
            print(str(i)+"  "+t)
            i = i + 1

        actual = []
        x = 0
        if("Specific Requests" in temp[1] or "Critical Calls" in temp[1]):
            actual.append(temp[0].split(":")[1][1:-1])          # report number
            actual.append(temp[1].split(":")[1][1:-1])          # section
            actual.append(temp[11].split(":")[1][1:-1])         # person
            actual.append(temp[4].split(":")[1][1:-1])          # qt
            actual.append(temp[5].split(":")[1][1:-1])          # description
            actual.append(temp[8].split(":")[1][1:-1])          # action comments
            actual.append(temp[10].split(":")[1][1:-1])         # comments
        elif("Bypass List" in temp[1]):
            actual.append(temp[0].split(":")[1][1:-1])          # report number
            actual.append(temp[1].split(":")[1][1:-1])          # section
            
            process = temp[6].split(":")[1][1:-1]

            for t in temp: 
                if(':' not in t):
                    x = x + 1
                    process = process + t 
            
            actual.append(temp[11 + x].split(":")[1][1:-1])         # person
            actual.append(temp[4].split(":")[1][1:-1])          # qt

            part = temp[8 + x].split(":")[1][1:-1]               
            if("\"" in temp[6].split(":")[1][1:-1]):
                process_format = process.replace("\",\""," \\ ")
                process_format = process_format.replace("\"\"",", ")
                process_format = process_format.replace("\""," ")
                process_format = process_format.replace("]","")
                process_format = process_format.replace(" ", "",1)
                actual.append(process_format + " - " + part)        # description
            actual.append(temp[9 + x].split(":")[1][1:-1])          
            actual.append(temp[10 + x].split(":")[1][1:-1])         # comments

        data.append(actual)
        
    write_excel(data)  
    txt = open(FILE_LOC + "FollowUp.txt",'w')
    txt.close() 
# ?------------------------------------------------ Write Excel File ------------------------------------------------- #
def write_excel(data):
    global DATA_FOLDER, XLSX_FILE
    print("# ----------------------------------------- Writing Excel ---------------------------------------- #")
    while(True):
        try:
            read_template = pd.read_excel(DATA_FOLDER + XLSX_FILE, engine='openpyxl') # open the template as pandas dataframe
            wb = load_workbook(DATA_FOLDER + XLSX_FILE)                               # load the workbook
            ws = wb.active                                                            # get the last active row
            next_row = ws.max_row + 1                                                 # get the next blank row after active row
            break                                                                     # break to rest of program once workbook is available
        except PermissionError:
            print("# --- Permission Error: Waiting for file to be accessible")
            continue                                                                  # keep trying to open workbook until available

    for d in data:      # iterate through data list (list of lists)
        read_template.at[next_row,'Unnamed: 0'] = d[0]                          # Report Num
        read_template.at[next_row,'Unnamed: 1'] = d[1]                          # Section
        read_template.at[next_row,'Unnamed: 2'] = d[2]                          # Follow Up Person
        read_template.at[next_row,'Daily Quality Audit Follow Up List'] = d[3]  # Quality Tech
        read_template.at[next_row,'Unnamed: 4'] = d[4]                          # Description
        read_template.at[next_row,'Unnamed: 5'] = d[5]                          # Action Taken
        read_template.at[next_row,'http://pmdadashboard/d/DluY5Ph4z/daily-shift-quality-audit-report?orgId=1&var-QA_ReportNo=All&from=now%2Fy&to=now%2Fy'] = d[6]
                                                                                # Follow Up Comments
        read_template.at[next_row,'Unnamed: 7'] = 'N'                           # Completed? 
        
        next_row = next_row + 1                                                 # increment row, to write on next row
    
    df_columns = read_template.shape[1]                                         # get columns                                                                               

    for r, row in enumerate(dataframe_to_rows(read_template,index=False, header=False),2):     # write to each points from dataframe to cells in excel
        for c in range(0,df_columns):
            try:
                ws.cell(row = r, column= c + 1).value = row[c]
            except AttributeError:
                pass
    
    for row in ws.iter_rows():         # apply formatting to each cell                                     
        for cell in row:
            cell.alignment = cell.alignment.copy(wrapText=True)         # apply text wrapping
            cell.alignment = cell.alignment.copy(vertical='center')     # apply vertical center

    while(True):
        try:
            wb.save(DATA_FOLDER + XLSX_FILE)                            # save the file
            break
        except PermissionError:                                         # keep trying until saving is possible
            continue
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                   Function Call                                                    #
# !------------------------------------------------------------------------------------------------------------------- #
timeout = 0
while(True):
    try:    
        file = glob(FILE_LOC + "*.txt")[0]                         # search for file
        print("# ------------------------------------------ File Found ------------------------------------------ #")         
        print("# --- Parsing File")
        parseFile(file)                                            # call parsefile function
        print("# --- Update Complete")
        break                                                      # if excel file was done and saved
    except:                     
        print("# ---" + str(Exception))
        sleep(10)
        timeout = timeout + 1
        if(timeout == 6):
            print("# ---------------------------------------- Time Out Error ---------------------------------------- #")
            break                                                  # program will timeout after 60 
        else:
            pass 