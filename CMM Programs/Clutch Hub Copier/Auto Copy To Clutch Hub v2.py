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
SRC = "C:\\Users\\sthakar\\Downloads\\PRISMO1" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "C:\\Users\\sthakar\\Documents\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\sthakar\\Documents\\Flatness Archive" """
#!Code Body------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def equator_copyPDF():
    global SRC, GF9_PATH, ARCHIVE
    while(True):  #to ensure it always runs in the background
        
        pdf_files = glob(SRC + "\\*.pdf") #get all PDF files from the source folder
        pdf_files.sort(key=path.getmtime, reverse=True)

        for pdf in pdf_files: #iterate through all files in source folder
            copy(pdf,GF9_PATH) #copy to N:\ Folder           
            move(pdf,ARCHIVE) #move pdf to ARCHIVE, leaves SRC folder empty


#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
equator_copyPDF()
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------
