#---IMPORT LIBRARIES---
import glob
import os
import pandas as pd
import pandas.io.formats.excel
pandas.io.formats.excel.ExcelFormatter.header_style = None
#-------------------------------------CODE BODY-------------------------------------------------

with open("C:/Users/Gleason/Downloads/Gleason_Python/PATHFILE_GLEASON.txt", 'r') as dir_source: #open .txt file to read file paths
    dir = dir_source.read().splitlines() #read all lines, split at  \n and discard \n from string usign .splitlines()
    
DEFAULT_PATH = dir[1] #this is the default file path for the csv file
print("DEFAULT PATH: "+DEFAULT_PATH)
SCRAP_PATH = dir[3] #path for the temp excel file
names = []

def isIn(str, array):

    for i in range(len(array)):
        if(str == array[i]):
            return 1
    return 0

def main():

    i = 0

    while(True):

        files = glob.glob(DEFAULT_PATH + '/*.csv') #read all files within DEFAULT_PATH with a .csv file extension 
        
        flag = -1
        
        for file in files:
        
            names.append(file[int(file.rfind("\\"))+1:]) #file last occurence of \\ to set the name
            i=i+1 #increment counter

            data = pd.read_csv(file) # read csv file
            data = data.T #transpose and overwrite csv file

            data_new = data.iloc[[3,4,6,9,15,21,26,42]] #take only certain rows
                                # 0,1,2,3, 4, 5, 6, 7
            
            data_new.index.values[0] = 'Date'
            data_new.index.values[1] = 'Time'
            data_new.index.values[2] = 'Part Number'
            data_new.index.values[3] = 'PD Runout'
            data_new.index.values[4] = 'Total Composite Action (TCV)'
            data_new.index.values[5] = 'Max Average Tooth to Tooth Composite Action (T2T AVG)'
            data_new.index.values[6] = 'Max functional Circular Tooth Thickness'
            data_new.index.values[7] = 'PD Nicks'
            
                    #index 3 - DATE - Date
                    #index 4 - TIME - Time
                    #index 6 - PART_NUMBER - Part_Number
                    #index 9 - PD_RUNOUT - PD_Runout
                    #index 15 - TCV - Total Composite Action (TCV)
                    #index 21 - AVG_WT2T - Max Average Tooth to Tooth Composite Action (T2T AVG)
                    #index 26 - MAX_TOL.5 - Max functional Circular Tooth Thickness
                    #index 42 - PD_Nicks - PD_Nicks

            XLSX_DIR = SCRAP_PATH + '/data.xlsx' #create new PATH for excel file

            writer = pd.ExcelWriter(XLSX_DIR) #open directory usign ExcelWriter (pandas)
            data_new.to_excel(writer, index = True, index_label='Chracteristics', header=False, sheet_name='Gleason_Report') #convert the data into excel format; store within new excel directory

            worksheet = writer.sheets['Gleason_Report'] #open excel sheet

            index_format = writer.book.add_format({'bold': True,'border':False,'align': 'left'})
            data_format = writer.book.add_format({'border':False,'align': 'right'})

            worksheet.set_column(0,0,53,index_format)
            worksheet.set_column(1,1,25,data_format)

            writer.save() #save file

            os.startfile(XLSX_DIR, "print") #print to default printer

            print("FILE PRINTED - "+names[i-1])

main()
