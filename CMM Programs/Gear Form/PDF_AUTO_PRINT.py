#Libraries-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob
from os import path,system
from datetime import datetime
from time import sleep
from subprocess import Popen
#Configuration-------------------------------------------------------------------------------------------------------------------------------------------------------------------
PDF_LOCATION = "C:\\Program Files (x86)\\Zeiss\\GearNT\\PDF" #set as location of pdf 
PDF_VIEWER = 'C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe'

#Functions-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
flag = 0
while(True):
   
    if flag == 0:
        print("----------------------------PROGRAM READY-------------------------------")
        flag = 1
        
    LAST_PRINTED_READ = open('C:\\Job\\Python\\Auto PDF Print\\LAST_FILE_PRINTED.txt','r') # open text file
                                                          # this file contains the file location of the last file printer
    last_file = LAST_PRINTED_READ.readlines() # save location to variable as type: list
    LAST_PRINTED_READ.close()
    
    try: 
        last_printed = last_file[0]
    except: 
        last_printed = ""
    
    pdf_files = glob(PDF_LOCATION + "\\**\\*.pdf") # find all files in subfolders from this directory
    newest_file = max(pdf_files, key=path.getmtime) # last modified file
    date_modified = str(datetime.fromtimestamp(path.getmtime(newest_file))) # save timestamp 

    if(newest_file != last_printed): # only pass through if the newest_file wasn't already printed

        print("\nLATEST FILE FOUND ---- "+newest_file)
        print("----DATE MODIFIED ---- "+date_modified)
      
        # {0} Acrobat Location {1} File Location. Last "" means it will print to default printer  
        cmd = '{0} /N /T "{1}" ""'.format(PDF_VIEWER,newest_file)
        print("\n----PRINTING IN PROGRESS")
        
        Popen(cmd) # run subprocess
        
        sleep(10) # sleep 
        system("TASKKILL /F /IM Acrobat.exe") # END Acrobat from Task Manager
        
        print("----REPORT PRINTED")
        print("\n------------------------------------------------------------------------")
        
        LAST_PRINTED_WRITE = open('C:\\Job\\Python\\Auto PDF Print\\LAST_FILE_PRINTED.txt','w')
        LAST_PRINTED_WRITE.write(newest_file) # update last printed file 
        LAST_PRINTED_WRITE.close()
        flag = 0 