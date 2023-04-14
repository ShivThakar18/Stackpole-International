
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
from os import remove
from datetime import datetime
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
# ?------------------------------------------------ Get File Function ------------------------------------------------ #
def getFile(): #* checks file source for new files; returns filename

    global LITMUS_DRIVE                                         # global LITMUS_DRIVE variable

    try:
        file = glob(LITMUS_DRIVE + "*.txt")[0]                  # looks for new text files, there should only be 1 at a time
    except:                                                     # except index out of range error when no new files
        print("No New Files")
        return ""                                               # return blank string
    
    print(file) 
    #time = datetime.timestamp(datetime.now())                   # get the current timestamp
    #rename(file,LITMUS_DRIVE+"FollowUp.txt")                    # rename the file with the timestamp at the end

    return LITMUS_DRIVE+"FollowUp.txt"                          # return this new file now
# ?------------------------------------------------- Parse Timestamp ------------------------------------------------- #
def parseTime(file): #* filename parser; returns the timestamp for given file
    
    index = file.rfind(".")                                    # find the index of the last '.' in the filename
    file = file[0:index]                                       # trim the entire file to include everything up to .txt

    return float(((file.split("\\")[-1]).split("_")[-1]))      # split the filename with the delimiters given
# ?---------------------------------------------------- Copy Data ---------------------------------------------------- #
def copyData(SRC,DEST): #* copies the data from the source file to the dest file

    src = open(SRC,'r')                                         # open source file for reading
    copy_to = src.read().splitlines()                           # read and split each line without \n at the end
    src.close()                                                 # close source file

    dest = open(DEST,'w')                                       # open dest file for appending

    for c in copy_to:                                           # iterate through the source file list
        dest.write(c)                                           # write each line to the master file
    dest.close()                                                # close the dest file
# ?---------------------------------------------------- Move File ---------------------------------------------------- #
def movefile(new): #* moves the file to the data folder

    global MASTER, DATA_FOLDER                                  # global variables

    new_time = parseTime(new)                                   # get the timestamp for the new file, call parseTime() function
    MASTER_time = parseTime(MASTER)                             # get the timestamp for the MASTER file, call parseTime() function

    new_file = DATA_FOLDER + path.basename(new)                 # new file needs a new path since it will be moved 
    copy(new,DATA_FOLDER)                                       # move the new file to the data folder
    copyData(new_file,MASTER)                                   # copy data to master, call copyData() function
    remove(new_file)                                            # remove the file from the directory
# ?------------------------------------------------- Refresh Master -------------------------------------------------- #
def refresh(): #! UNUSED - clears the MASTER file every 2 days

    global MASTER                                               # global MASTER variable
    MASTER = glob(DATA_FOLDER + "MASTER_*.txt")[0]              # use glob to find the text files with the following criteria

    master_time = parseTime(MASTER)                             # get time; use parseTime() function
    now = datetime.timestamp(datetime.now())                    # get the current timestamp

    diff = abs(float(now) - float(master_time))                 # find the difference between both timestamps

    diff = datetime.fromtimestamp(diff)                         # convert to datetime format
                                                                # this will return a date from 1970
                                                                # the timestamp at 0 is equal to Jan 1st 1970 at midnight
                                                                # the timestamp is every second after that date/time
    days = int(diff.strftime("%d"))                             # convert to time

    if(days >= 3):                                              # if the time difference is 3 days
        m = open(MASTER,'r')                                    # open the master file for reading
        m_read = m.read().splitlines()                          # read each line
        m.close()                                               # close the master file

        temp = []                                               # temp list that holds incomplete follow up actions
        for mr in m_read:                                       # iterate through each line
            if(mr[-1] == "0"):                                  # if incomplete, append to temp list
                temp.append(mr)
        
        m = open(MASTER,'w')                                    # open master file for writing
        for t in temp:                                          # iterate through temp list
            m.write(t+"\n")                                     # write each line to file with \n at the end
        m.close()                                               # close master file

        temp_name = DATA_FOLDER + "MASTER_"+str(datetime.timestamp(datetime.now()))+".txt"    
                                                                # give new name to master with new timestamp
        rename(MASTER,temp_name)                                # rename master file
        MASTER = temp_name                                      # set the file
    else:                                                       # if less than 3 days
        print("MASTER Up To Date")                                                              
# ?------------------------------------------------ Parse and Extract ------------------------------------------------ #
def parseFile():

    global MASTER                                                   # call global variable into scope

    #MASTER = glob(DATA_FOLDER + "MASTER_*.txt")[0]                  # get the master file

    FILE = glob(DATA_FOLDER + "FollowUp.txt")
    m_file = open(FILE[0],'r')                                       #
    m_data = m_file.read().splitlines()
    m_file.close()

    for i in range(len(m_data)):
        m_data[i] = m_data[i][1:-1]
    

    data = []
    temp = []

    for m in m_data:
        temp = m.replace(",\"","|\"")
        temp = temp.split("|")

        actual = []
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
            actual.append(temp[11].split(":")[1][1:-1])         # person
            actual.append(temp[4].split(":")[1][1:-1])          # qt

            process = temp[6].split(":")[1][1:-1]
            part = temp[8].split(":")[1][1:-1]

            if("\"" in temp[6].split(":")[1][1:-1]):
                process_format = process.replace("\"","")
                actual.append(process_format + " - " + part)

            actual.append(temp[9].split(":")[1][1:-1])          
            actual.append(temp[10].split(":")[1][1:-1])         # comments

        data.append(actual)
        
    write_excel(data)    
# ?------------------------------------------------ Write Excel File ------------------------------------------------- #
def write_excel(data):
    global DATA_FOLDER, XLSX_FILE
    print("writing excel")
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
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                   Function Call                                                    #
# !------------------------------------------------------------------------------------------------------------------- #
while(True): #* run infinitely
    #file = getFile()                                             # check for new files
    file = DATA_FOLDER + "FollowUp.txt"
    if(file == ""):                                              # if no files found; continue
        continue                                                 # skip to next iteration
    else:                                                        # if new file is found
        print("File Found - "+file)
        #movefile(file)                                           # call movefile function
        #move(file,DATA_FOLDER)
        print("parsing file")
        parseFile()
        #remove(DATA_FOLDER + "FollowUp.txt")
        break
        """ new_file = open(LITMUS_DRIVE + "FollowUp.txt","w")
        new_file.close() """
        

    
