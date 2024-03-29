
#! ------------------------------------------------- Import Libraries ------------------------------------------------- #
from glob import glob
from shutil import move,copy
from os import path, startfile,rename
import pandas as pd
import pandas.io.formats.excel
from time import sleep
from datetime import datetime
pandas.io.formats.excel.ExcelFormatter.header_style = None

#! ------------------------------------------------- Global Variables ------------------------------------------------- #
#PATHFILE = open("C:\\Users\\Gleason\\Downloads\\Gleason_Python\\PATHFILE_GLEASON.txt","r")      # read file that contains filepaths
ARCHIVE = "C:\\Users\\Gleason\\Documents\\Gleason Archive\\"
ARCHIVE = "C:\\Users\\vrerecich\\Documents\\Gleason Archive\\"
DIRECTORY = ["","","",""]#PATHFILE.read().splitlines()                                                        # save each line from the text file to variable

DEFAULT_PATH = DIRECTORY[1]         # default directory 
DEFAULT_PATH = "C:\\Users\\vrerecich\\Documents\\Gleason Data"
SCRAP_PATH = DIRECTORY[3]           # scrap path contains a temporary data excel file
SCRAP_PATH = "C:\\Users\\vrerecich\\Desktop\\Stackpole_Internationl_Repo\\Stackpole-International\\CMM Programs\\Gleason\\Scrap"
#? --------------------------------------------- Convert To Excel Function -------------------------------------------- #
def csv2xlsx(file): 
    data = pd.read_csv(file)        # create a dataframe using pandas from csv found
    data = data.T                   # transpose dataframe (rows = columns, columns = rows)
    
    data_new = data.iloc[[3,4,6,9,15,21,26,42]]         # extract specific rows from
                # RowNums 4,5,7,10,16,22,27,43
    
    data_new.index.values[0] = 'Date'                                                       # Row 04 of CSV, Row 1 of XLSX
    data_new.index.values[1] = 'Time'                                                       # Row 05 of CSV, Row 2 of XLSX
    data_new.index.values[2] = 'Part Number'                                                # Row 07 of CSV, Row 3 of XLSX
    data_new.index.values[3] = 'PD Runout'                                                  # Row 10 of CSV, Row 4 of XLSX
    data_new.index.values[4] = 'Total Composite Action (TCV)'                               # Row 16 of CSV, Row 5 of XLSX
    data_new.index.values[5] = 'Max Average Tooth to Tooth Composite Action (T2T AVG)'      # Row 22 of CSV, Row 6 of XLSX
    data_new.index.values[6] = 'Max functional Circular Tooth Thickness'                    # Row 27 of CSV, Row 7 of XLSX
    data_new.index.values[7] = 'PD Nicks'                                                   # Row 43 of CSV, Row 8 of XLSX

    partNum = data_new[0]['Part Number']    
    print(partNum)

    XLSX_DIR = SCRAP_PATH + "\\data.xlsx"        # save file path

    writer = pd.ExcelWriter(XLSX_DIR)           # create excel file using pandas ExcelWriterr using new path
    data_new.to_excel(writer, index = True, index_label='Chracteristics', header=False, sheet_name='Gleason_Report') # convert the data into excel format; store within new excel directory

    worksheet = writer.sheets['Gleason_Report'] # open excel sheet

    index_format = writer.book.add_format({'bold': True,'border':False,'align': 'left'})        # formatting columns
    data_format = writer.book.add_format({'border':False,'align': 'right'})

    worksheet.set_column(0,0,53,index_format)       # formatting columns
    worksheet.set_column(1,1,25,data_format)

    writer.save() # save file
    writer.close()

    name = str(partNum) + " " +str(datetime.now().strftime("%m_%d_%Y_%H_%M_%S")) + ".xlsx"
    sleep(2)
    rename(XLSX_DIR,SCRAP_PATH+"\\"+name)
    sleep(3)
    startfile(SCRAP_PATH+"\\"+name, "print") # print to default printer
    sleep(5)
    move(SCRAP_PATH+"\\"+name,ARCHIVE)
    sleep(5)
#! --------------------------------------------------- Function Call -------------------------------------------------- #
while(True):


    files = glob(DEFAULT_PATH + '\\*.csv')
    if(len(files) > 0):
        new = max(files, key= path.getmtime)          # get the newest file
        csv2xlsx(new)                                                           
    else:
        continue
