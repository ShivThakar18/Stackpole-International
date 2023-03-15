
# *------------------------------------ Shiv Thakar - Quality Engineering Intern ------------------------------------- #
# *--------------------------------------------- Stackpole International --------------------------------------------- #
# *------------------------------------ Daily Quality Audit Follow Up Application ------------------------------------ #
# *---------------------------------------------- Date: March 2nd, 2023 ---------------------------------------------- #
# !------------------------------------------------------------------------------------------------------------------- #
# !                                               Import Python Modules                                                #
# !------------------------------------------------------------------------------------------------------------------- #
from os import path, rename
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
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                 Define Variables                                                   #
# !------------------------------------------------------------------------------------------------------------------- #
LITMUS_DRIVE = "L:\\ShivDataOutput\\Daily_Quality_Audits\\Follow_Up\\"                      # file source
DATA_FOLDER = "N:\\Quality\\Personal Folders for Quality Staff\\Shiv\\Audit_Data_Folder\\"  # file dest
MASTER = ""                                                                                 # master file name, initially empty
XLSX_FILE = "Audit Follow Up List.xlsx"
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                     Functions                                                      #
# !------------------------------------------------------------------------------------------------------------------- #
# ?------------------------------------------------ Parse and Extract ------------------------------------------------ #
def parseFile():

    global MASTER                                                   # call global variable into scope

    MASTER = glob(DATA_FOLDER + "MASTER_*.txt")[0]                  # get the master file

    m_file = open(MASTER,'r')                                       #
    m_data = m_file.read().splitlines()
    m_file.close()


    for i in range(len(m_data)):
        m_data[i] = m_data[i][1:-2]

    data = []
    temp = []
    actual = []

    for m in m_data:
        temp = m.split(",")
        
        actual.append(temp[0].split(":")[1][1:-1])          # report number
        actual.append(temp[1].split(":")[1][1:-1])          # section
        actual.append(temp[12].split(":")[1][1:-1])         # person
        actual.append(temp[4].split(":")[1][1:-1])          # qt
        actual.append(temp[5].split(":")[1][1:-1])          # description
        actual.append(temp[8].split(":")[1][1:-1])          # action comments
        actual.append(temp[10].split(":")[1][1:-1])         # comments

        data.append(actual)

    write_excel(data)    
# ?------------------------------------------------ Write Excel File ------------------------------------------------- #
def write_excel(data):

    global DATA_FOLDER, XLSX_FILE

    while(True):
        try:
            read_template = pd.read_excel(DATA_FOLDER + XLSX_FILE, engine='openpyxl')
            wb = load_workbook(DATA_FOLDER + XLSX_FILE)
            ws = wb.active
            next_row = ws.max_row + 1
            break
        except PermissionError:
            print("Permission Error")
            continue       
            sleep(10)

    for d in data: 

        read_template.at[next_row,'Unnamed: 0'] = d[0]
        read_template.at[next_row,'Unnamed: 1'] = d[1]
        read_template.at[next_row,'Unnamed: 2'] = d[2]
        read_template.at[next_row,'Daily Quality Audit Follow Up List'] = d[3]
        read_template.at[next_row,'Unnamed: 4'] = d[4]
        read_template.at[next_row,'Unnamed: 5'] = d[5]
        read_template.at[next_row,'Unnamed: 6'] = d[6]
        read_template.at[next_row,'Unnamed: 7'] = 'N'
        
        next_row = next_row + 1
    
    df_columns = read_template.shape[1]

    for r, row in enumerate(dataframe_to_rows(read_template,index=False, header=False),2):
        for c in range(0,df_columns):
            try:
                ws.cell(row = r, column= c + 1).value = row[c]
            except AttributeError:
                pass
    
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = cell.alignment.copy(wrapText=True)
            cell.alignment = cell.alignment.copy(vertical='center')


    while(True):
        try:
            wb.save(DATA_FOLDER + XLSX_FILE)
            break
        except PermissionError:
            continue

parseFile()