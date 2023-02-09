#Import Required Python Modules----------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob 
from shutil import copy,move
from os import path,rename
from time import localtime, strftime
#!File Paths-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SRC = "C:\\Users\\PRISMO1\\Downloads" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "N:\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
#!Exists Function------------------------------------------------------------------------------------------------------------------------------------------------------------------
def exists(filepath): #* functions checks if the file already exists in the destination folder ~ GF9_PATH
    global GF9_PATH
    pdf_file = path.basename(filepath) #get only the file name
    
    gf9 = glob(GF9_PATH+"\\*.pdf") #get all files in destination folder
    gf9.sort(key=path.getmtime, reverse=True)
    
    for f in gf9:
        if(path.basename(f) == path.basename(filepath)):
            return 0
        
    return 1 #if it doesn't exists return FALSE
#!Code Body------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def equator_copyPDF():
    global SRC
    while(True):  #to ensure it always runs in the background
        pdf_files = glob(SRC + "\\*.pdf") #get all PDF files from the source folder
        pdf_files.sort(key=path.getmtime, reverse=True)
        for pdf in pdf_files: #iterate through all files in source folder

            check = exists(pdf)

            if(check == 0): #call exists() function to check if the file has already been copied    
                continue #if it exists, go to next file
            
            else:
                copy(pdf,GF9_PATH) #if it doesn't exists, copy the file
                print("COPIED - "+path.basename(pdf))
        
#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
equator_copyPDF()
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------
