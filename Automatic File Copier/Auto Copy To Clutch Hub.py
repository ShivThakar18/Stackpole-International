#Import Required Python Modules----------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob 
from shutil import copy
from os import path
#!File Paths-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SRC = "C:\\Users\\PRISMO1\\Downloads" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "N:\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 

#!Exists Function------------------------------------------------------------------------------------------------------------------------------------------------------------------
def exists(filepath): #* functions checks if the file already exists in the destination folder ~ GF9_PATH

    pdf_file = filepath.split("\\")[-1] #get only the file name
    
    gf9 = glob(GF9_PATH+"\\*.pdf") #get all files in destination folder

    for f in gf9: #iterate through destination folder
        if(f.split("\\")[-1] == pdf_file): #check if the passed file exists
            return True #if it exists TRUE
            
    return False #if it doesn't exists return FALSE
#!Code Body------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def equator_copyPDF():
    while(True):  #to ensure it always runs in the background
        pdf_files = glob(SRC + "\\*.pdf") #get all PDF files from the source folder

        for pdf in pdf_files: #iterate through all files in source folder
            if(exists(pdf)): #call exists() function to check if the file has already been copied
                continue #if it exists, go to next file
            
            copy(pdf,GF9_PATH) #if it doesn't exists, copy the file
            print("COPIED - "+path.basename(pdf))
#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
equator_copyPDF()
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------