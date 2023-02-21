#Import Required Python Modules----------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob 
from shutil import copy,move
from os import path,rename
from datetime import datetime
#!File Paths-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SRC = "C:\\Users\\PRISMO1\\Downloads" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "N:\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\PRISMO1\\Documents\\Flatness Archive"

""" #For Testing
SRC = "C:\\Users\\vrerecich\\Downloads\\PRISMO1" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "C:\\Users\\vrerecich\\Documents\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\vrerecich\\Documents\\Flatness Archive" """
#!Code Body------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def equator_copyPDF():
    global SRC, GF9_PATH, ARCHIVE
    while(True):  #to ensure it always runs in the background
        
        pdf_files = glob(SRC + "\\*.pdf") #get all PDF files from the source folder
        pdf_files.sort(key=path.getmtime, reverse=True)

        for pdf in pdf_files: #iterate through all files in source folder

            new_name = SRC + "\\" + path.basename(pdf)[0:-4] + "_" + datetime.fromtimestamp(path.getmtime(pdf)).strftime('%Y_%m_%d') +'.pdf'
            rename(pdf, new_name) #rename pdf to new_name
            
            copy(new_name,GF9_PATH) 
            print("COPIED - "+path.basename(pdf))
            
            '''
            move files to an archive right away
            ''' 

            move(new_name,ARCHIVE)


#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
equator_copyPDF()
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------
