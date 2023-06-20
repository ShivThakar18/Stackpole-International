#  -------------------------------------------------------------------------------------------------------------------- #
#* ---------------------------------------------------- Shiv Thakar --------------------------------------------------- #
#* ----------------------------------------------------- Jomesa 5 ----------------------------------------------------- #
#* ------------------------------------------ Stackpole International - PMDA ------------------------------------------ #
#* -------------------------------------------- Quality Engineering Intern -------------------------------------------- #
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                Import Python Libraries                                               #
#! -------------------------------------------------------------------------------------------------------------------- #
from os import path
from shutil import copy
from glob import glob
from pdfminer.high_level import extract_text
import pdfplumber
from time import time                   
from Jomesa5_Settings import DIRECTORY, LE_DIR, LOCALDATA_ARCHIVE,YEAR,ARCHIVE_FILE          #? import variables from Jomesa5_Settings
#! ---------------------------------------------- Define Global Variables --------------------------------------------- #
DIR_10R140 = DIRECTORY + "10R140 Components\\"
PARTS = ['10R140 Body', '10R140 Slide', '10R140 Rotor']
ARCHIVE_FILE = ARCHIVE_FILE + "Archived_10R140_"+YEAR+".txt"
#? ---------------------------------------------------- 10R140 Data --------------------------------------------------- #
def get10R140Data(report):
    
    global PARTS,ARCHIVE_FILE

    if('Point of Ship' in report):              # check file path to check the location of sample
        LOCATION = 'Point of Ship'              # set location to "Point of Ship"
    elif('Straight From Washer' in report):     
        LOCATION = 'Straight From Washer'       # set location to Straight From Washer
    elif('Eng Trials' in report):
        LOCATION = 'Eng Trials'                 # set location to Eng Trials
    else:
        LOCATION = ''

    if('Pass' in report):                       # depending on what is stated in the file name
        RESULT = 'PASS'                         # set Pass
    elif('Fail' in report):
        RESULT = 'FAIL'                         # set Fail

    text = extract_text(report)                 # using pdfminer.high_level extract_text function, extract text from pdf report
    with pdfplumber.open(report) as pdf:        # pdfplumber open report and extract table
        page = pdf.pages[0]
        table = page.extract_table()
    
    varadd = 5                                  # predefined incrementer that helps to find the actual value we are looking for 
    content = str(text).split("\n")             # split extracted text at each line
    #pprint(content)

    for i in range(len(content)):               # iterate through content using length operation

        if (content[i] == 'Component:'):        
            PART_NAME = content[i+varadd]       # save Part Name
            if('-' in PART_NAME or '.' in PART_NAME):
                PART_NAME = [p for p in PARTS if(p in report)][0]
                
        if (content[i] == 'Sample No.:'):
            REPORT_NO = content[i+varadd]       # save Report Number

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

        if (content[i] == 'Date of Analysis:'):
            DATE = content[i+varadd]            # save Date
            
            timeout = time() + 60*0.2

            while(any(c.isalpha() for c in DATE.replace("/","")) or DATE == ''):

                if('/' not in DATE):                # account for different values within DATE
                    DATE = content[i+varadd+1]
                if(any(c.isalpha() for c in DATE.replace("/","")) == True):
                    DATE =content[i+varadd-1]
                if(time() >= timeout):
                    print("TIMEOUT, NO DATE FOUND")
                    DATE = "//"
                    break
            
            date_mod =  DATE.split("/")
            DATE = date_mod[1] + "/" + date_mod[0] + "/" + date_mod[2]      # change format
            
        if (content[i] == 'Weight [mg]:'):      
            WEIGHT = content[i+varadd]                                      # save weight
            if(any(c.isalpha() for c in WEIGHT)):
                WEIGHT = ""

        if ('Occupancy[%]:' in content[i] and 'Allowed' not in content[i]):
            OCCUPANCY = content[i].split(": ")[1]                           # save occupancy

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
            if(any(not c.isdigit() for c in TOTAL_FIBERS)):
                TOTAL_FIBERS = ''

        if('Passes Specification' in content):
            RESULT = 'PASS'

        if ('Does Not Pass Specification' in content):
            RESULT = 'FAIL'

    for block in table:                 # iterate through table per block     
        for i in range(len(block)):     
            if(block[i] == 'J-K'):      
                JK = block[i+5]         # save JK spec from report

            if(block[i] == 'H-I'):
                HI = block[i+5]         # save HI spec from report

            if(block[i] == 'F-G'):
                FG = block[i+5]         # save FG spec from report

            if(block[i] == 'C-E'):
                CE = block[i+5]         # save CE spec from report
    
    # save all extracted points in a list
    DATALIST = [DATE,REPORT_NO,LOCATION,PART_NAME,JK,HI,FG,CE,WEIGHT,OCCUPANCY,METALLIC_LEN,METALLIC_WIDTH,NON_METALLIC_LEN,NON_METALLIC_WIDTH,FIBER_LEN,TOTAL_FIBERS,RESULT]
    
    # write file path to archive list
    ARCHIVE_LIST = open(ARCHIVE_FILE,'a+')       # open current year archive list for reading
    ARCHIVE_LIST.write(report+"\n")
    ARCHIVE_LIST.close()                                                 # close file, data already extracted on Line 98

    # write DATALIST to text file with the report number

    if('2023' in report):
        y = "2023"
    if('2022' in report):
        y = "2022"
    if('2021' in report):
        y = "2021"
    if('2020' in report):
        y = "2020"

    dataFilename = LOCALDATA_ARCHIVE+REPORT_NO+"_"+y+"_"+PART_NAME+"_DATA.txt"          # write to local data archive

    DATA_FILE = open(dataFilename,"w")
    DATA_FILE.write(",".join(DATALIST))
    DATA_FILE.close()

    copy(dataFilename,LE_DIR)                   # copy data file to LE drive
    copy(report,LE_DIR)                         # copy report to LE drive
#? ----------------------------------------------- Search 10R140 Folders ---------------------------------------------- #
def search10R140():
    global PARTS,ARCHIVE_FILE           # bring global variables into scope

    # N:\Quality\Metlab\Met Lab Reports\Sediment Tests\Jomesa results\10R140 Components
                            #  \10R140 Body\2023\2023 [Eng Trials,Point of Ship, Straight From Washer]
                            #  \10R140 Slide\2023\2023 [Eng Trials,Point of Ship, Straight From Washer]
                            #  \10R140 Rotor\2023\2023 [Eng Trials,Point of Ship, Straight From Washer]

    filesList = []      # will be a list of 3 elements, 
                        # will hold the latest file from each part
                        # if a folder is empty, then it will have less elements
                        # in theory should have 3 always, unless new year

    for p in PARTS:     # iterate through all parts
        
        f = glob(DIR_10R140+p+"\\"+YEAR+"\\**\\*.pdf") # get the files using glob operation

        try:
            latest = max(f,key= path.getmtime)          # save the latest file from each part
            filesList.append(latest)                      # append to file list   [Body, Slide, Rotor]
        except ValueError:                                # if there is no files in directory, a value error is raised, 
                                                          # except this error, pass
            pass

    ARCHIVE_LIST = open(ARCHIVE_FILE,'r')       # open current year archive list for reading
    archived = ARCHIVE_LIST.read().splitlines()                             # data extraction using read().splitlines() (remove \n from ends)
    ARCHIVE_LIST.close()                                                    # close file, data already extracted on Line 98

    remove_list = []
    # This snippet of code cross references the archive list and latest files
    for f in filesList:
        for a in archived:
            if(f == a):                                     # latest files == an archived file
                print("MSG: File Already Exists")  
                remove_list.append(f)                         # remove from filesList
                break

    for r in remove_list:
        if(r in filesList):
            filesList.remove(r)

    if(len(filesList) == 0):
        return []                                           # if the length is ZERO, this means that there are no new files

    print("MSG: New File Found - "+str(filesList))
    return filesList                                        # else, there is new files and the files list and a flag is passed
