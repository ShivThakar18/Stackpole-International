#  -------------------------------------------------------------------------------------------------------------------- #
#* ---------------------------------------------------- Shiv Thakar --------------------------------------------------- #
#* ----------------------------------------------------- Jomesa 5 ----------------------------------------------------- #
#* ------------------------------------------ Stackpole International - PMDA ------------------------------------------ #
#* -------------------------------------------- Quality Engineering Intern -------------------------------------------- #
"""DATA LIST SUMMARY
    DATALIST = 
            [0] DATE
            [1] REPORT_NO
            [2] PART_NAME
            [3] K
            [4] J
            [5] I
            [6] H
            [7] WEIGHT
            [8] NUM_COMPONENTS
            [9] METALLIC_LEN
            [10] METALLIC_WIDTH
            [11] NON_METALLIC_LEN
            [12] NON_METALLIC_WIDTH
            [13] FIBER_LEN
            [14] TOTAL_FIBERS
"""
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                Import Python Libraries                                               #
#! -------------------------------------------------------------------------------------------------------------------- #
from os import path
from shutil import copy
from glob import glob
from pdfminer.high_level import extract_text
import pdfplumber
from time import time       
from pprint import pprint            
from Jomesa5_Settings import DIRECTORY, LE_DIR, LOCALDATA_ARCHIVE,YEAR,ARCHIVE_FILE          #? import variables from Jomesa5_Settings
#! ---------------------------------------------- Define Global Variables --------------------------------------------- #
DIR_GME = DIRECTORY + "GME T4 Stator\\"
ARCHIVE_FILE = ARCHIVE_FILE + "Archived_GMET4_"+YEAR+".txt"
LOCALDATA_ARCHIVE = LOCALDATA_ARCHIVE + "GME T4 Stator\\"                  # directory for local data archive
#? ----------------------------------------------------- GME Data ----------------------------------------------------- #
def getGMEData(report):

    global ARCHIVE_FILE

    text = extract_text(report)
    with pdfplumber.open(report) as pdf: 
        page = pdf.pages[0]
        table = page.extract_table()
    
    content = str(text).split("\n")

    varadd = 5

    for i in range(len(content)):

        if(content[i] == 'Component:'):
            PART_NAME = content[i+varadd]

        if(content[i] == 'Sample No.:'):
            REPORT_NO = content[i+varadd]                               # save report name
        
            if('-' not in REPORT_NO and 'ST' not in REPORT_NO):
                for c in content:
                    if('ST' in c and '-' in c):
                        stripped = c.replace(" ","")
                        start = stripped.find('S')
                        length = 9
                        REPORT_NO = stripped[start:start+length]
        
            if(len(REPORT_NO) > 9):
                stripped = REPORT_NO.replace(" ","")
                start = stripped.find('S')
                length = 9
                REPORT_NO = stripped[start:start+length]
    
        if(content[i] == 'Date of Analysis:'):
            DATE = content[i+varadd]
            timeout = time() + 60*0.2

            while(any(c.isalpha() for c in DATE.replace("/","")) or DATE == ''):

                if('/' not in DATE):                # account for different values within DATE
                    DATE = content[i+varadd+1]
                if(any(c.isalpha() for c in DATE.replace("/","")) == True):
                    DATE =content[i+varadd-1]
                if(time() >= timeout):
                    DATE = "//"
                    for c in content:
                        if(c.count('/') == 2 and '20' in c):
                            DATE = c
                    if(DATE == '//'):
                        print("TIMEOUT, NO DATE FOUND")
                        break
            
            date_mod =  DATE.split("/")
            DATE = date_mod[2] + "-" + date_mod[1] + "-" + date_mod[0]      # change format YYYY-MM-DD

        if(content[i] == 'Weight [mg]:'):
            WEIGHT = content[i+varadd]
            if(any(c.isalpha() for c in WEIGHT.replace(".",""))):
                    WEIGHT = ""

        if(content[i] =='Components on filter:'):
            NUM_COMPONENTS = content[i+varadd-1]

        if ('Largest metallic particle' in content[i] and i == [idx for idx, s in enumerate(content) if 'Largest metallic particle' in s][0]):              # find string in list, but make sure it is the first occurance of the substring
                METALLIC_LEN = content[content.index('Length [µm]:') + 3]      # save largest metallic length
                METALLIC_WIDTH = content[content.index('Width [µm]:') + 3]            # save largest metallic width

        if ('Largest nonmetallic particle' in content[i] and i == [idx for idx, s in enumerate(content) if 'Largest nonmetallic particle' in s][0]):        # find string in list, but make sure it is the first occurance of the substring
            NON_METALLIC_LEN = content[max(loc for loc, val in enumerate(content) if val == 'Length [µm]:') + 3]        # save largest nonmetallic width
            NON_METALLIC_WIDTH = content[max(loc for loc, val in enumerate(content) if val == 'Width [µm]:')+3]         # save largest nonmetallic width

        if ('Length of largest fiber' in content[i] and i == [idx for idx, s in enumerate(content) if 'Length of largest fiber' in s][0]):                  # find string in list, but make sure it is the first occurance of the substring
            FIBER_LEN = content[i+2]            # save fiber length
            if(any(not c.isdigit() for c in FIBER_LEN)):
                FIBER_LEN = ''
        if ('Total length of fibers' in content[i] and i == [idx for idx, s in enumerate(content) if 'Total length of fibers' in s][0]):                    # find string in list, but make sure it is the first occurance of the substring
            TOTAL_FIBERS = content[i+2]         # save total length of fibers
        
    K = ""
    J = ""
    I = ""
    H = ""
    for block in table: 
        for i in range(len(block)):
            if(block[i] == 'K'):
                K = block[i+1]
            if(block[i] == 'J'):
                J = block[i+1]
            if(block[i] == 'I'):
                I = block[i+1]
            if(block[i] == 'H'):
                H = block[i+1]
    
    DATALIST = [DATE,REPORT_NO,PART_NAME,K,J,I,H,WEIGHT,NUM_COMPONENTS,METALLIC_LEN,METALLIC_WIDTH,NON_METALLIC_LEN,NON_METALLIC_WIDTH,FIBER_LEN,TOTAL_FIBERS]

    ARCHIVE_LIST = open(ARCHIVE_FILE,'a+')
    ARCHIVE_LIST.write(report+"\n")
    ARCHIVE_LIST.close()

    dataFilename = LOCALDATA_ARCHIVE+REPORT_NO+"_"+YEAR+"_"+PART_NAME+"_DATA.txt"          # write to local data archive

    DATA_FILE = open(dataFilename,"w")
    DATA_FILE.write(",".join(DATALIST))
    DATA_FILE.close()

    copy(dataFilename,LE_DIR)                   # copy data file to LE drive
    #copy(report,LE_DIR)                         # copy report to LE drive   
#? ------------------------------------------------- Search GME Folder ------------------------------------------------ #
def searchGME():

    global ARCHIVE_FILE

    filesList = [] 

    f = glob(DIR_GME+"\\"+YEAR+"\\*.pdf")

    try:
        latest = max(f,key=path.getmtime)
        filesList.append(latest)
    except ValueError:
        pass

    ARCHIVE_LIST = open(ARCHIVE_FILE,'r')
    archived = ARCHIVE_LIST.read().splitlines()
    ARCHIVE_LIST.close()

    remove_list = []
    for f in filesList:
        for a in archived:
            if(f == a):
                remove_list.append(f)
                break
    
    for r in remove_list:
        if(r in filesList):
            filesList.remove(r)
    
    if(len(filesList) == 0):
        return []

    print("MSG: New File Found - "+ str(filesList))
    return filesList
#? ------------------------------------------------ Find All GME Files ------------------------------------------------ #
def findAll():
    files = []

    f = glob(DIR_GME+"\\**\\*.pdf")
    files.extend(f)

    return files

""" report = "N:\\Quality\\Metlab\\Met Lab Reports\\Sediment Tests\\Jomesa results\\GME T4 Stator\\2023\\"
files = ['ST23-459','ST23-466','ST23-468','ST23-473','ST23-474','ST23-476','ST23-477','ST23-485']

for f in files: 

    getGMEData(report+f+".pdf")
    print(f) """