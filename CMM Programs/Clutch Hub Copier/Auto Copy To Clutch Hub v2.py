#Import Required Python Modules----------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob 
from shutil import copy,move
from os import path,rename
from datetime import datetime
#!File Paths-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SRC = "C:\\Users\\PRISMO1\\Downloads" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "N:\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\PRISMO1\\Documents\\Flatness Archive"
ERROR = ARCHIVE + "\\Error Files"
LOG = "N:\\Quality\\Personal Folders for Quality Staff\\Shiv\\CMM Program Logs\\Flatness Scan Log.txt"
""" #For Testing
SRC = "C:\\Users\\sthakar\\Downloads\\PRISMO1" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "C:\\Users\\sthakar\\Documents\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\sthakar\\Documents\\Flatness Archive" """
COUNT = 0
#!Code Body------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def equator_copyPDF():
    global SRC, GF9_PATH, ARCHIVE,COUNT       
    pdf_files = glob(SRC + "\\*.pdf") #get all PDF files from the source folder
    for pdf in pdf_files: #iterate through all files in source folder
        try: # already exists
            copy(pdf,GF9_PATH) #copy to N:\ Folder           
            move(pdf,ARCHIVE) #move pdf to ARCHIVE, leaves SRC folder empty
            print("COPIED - "+pdf)
            COUNT = COUNT + 1
        except:
            try:
                move(pdf,ERROR)
            except:
                continue
            continue

    print("Complete")


#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
print("Program Ready")
log_file = open(LOG,'a')
equator_copyPDF()
log_file.write(str(datetime.now()) + " - Transfer Complete. # of Files = "+str(COUNT)+"\n")
log_file.close()
    
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------
