#Import Required Python Modules----------------------------------------------------------------------------------------------------------------------------------------------------
from glob import glob 
from shutil import copy,move
from os import path,rename
from time import localtime, strftime
#!File Paths-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SRC = "C:\\Users\\PRISMO1\\Downloads" #? Prismo1 PC Directory - All Equator Reports saved here
GF9_PATH = "N:\\GF9 Clutch Hub\\Flatness Scans" #? Copy these files to network drive for easy access 
ARCHIVE = "C:\\Users\\PRISMO1\\Documents\\Flatness Archive"
#!Exists Function------------------------------------------------------------------------------------------------------------------------------------------------------------------
def exists(filepath): #* functions checks if the file already exists in the destination folder ~ GF9_PATH
    global GF9_PATH,ARCHIVE
    pdf_file = path.basename(filepath) #get only the file name
    
    gf9 = glob(GF9_PATH+"\\*.pdf") #get all files in destination folder
    gf9.sort(key=path.getmtime, reverse=True)
    
    for f in gf9:
        if(path.basename(f) == path.basename(filepath)):

            '''
            file date checker
            since files can have the same name, it must be replaced with the new one
            '''

            src_date = path.getmtime(filepath)
            dest_date = path.getmtime(f)

            if(src_date > dest_date): #if source file is newer
                convert_time = localtime(dest_date)
                format_time = strftime('%Y_%M_%D',convert_time) 
                rename(f, f + "_"+format_time) #rename old file with its date and time
                move(f, ARCHIVE+"\\"+path.basename(f+ "_"+format_time)) #move old file to archive
                return 1

            if(src_date <= dest_date):
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

                '''
                move files to an archive right away
                '''
        
#!Main Function Call---------------------------------------------------------------------------------------------------------------------------------------------------------------
equator_copyPDF()
#!End of Python Script-------------------------------------------------------------------------------------------------------------------------------------------------------------
