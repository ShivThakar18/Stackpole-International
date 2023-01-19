'''
' Shiv Thakar - Quality Engineer Intern
' Stackpole International
' ERS Terminal Setup
'''
#!Import Modules--------------------------------------------------------------------------------------------------------------------------------------------------------------------
from os import mkdir,rmdir,path,rename,remove
from shutil import move
from glob import glob
from zipfile import ZipFile
import winshell
import win32com.client

#!Set Directories----------------------------------------------------------------------------------------------------------------------------------------------------------------------
folder_loc = 'C:\\Users\\Public\\ERS Stackpole\\'               # FOLDER IS CREATED IN PUBLIC FOLDER
zip_loc = 'N:\\Quality\\Personal Folders for Quality Staff\\Shiv\\ERS Terminal.zip' # This is a zip that may be updated by the developer (ME)
                                                                                    # This file holds the latest version of the ERS Terminal

#!Functions----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?Setup--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def setup(prev): #the initial set up of the terminal
    
    try: # create a new folder
        print("Creating new folder "+folder_loc)
        mkdir(folder_loc)
    except: # exception raised if folder already exists
        print("Folder already exists")
        initial_failed() # call initial_failed
        return

    print("Preparing ZIP File for extraction")
    with ZipFile(zip_loc,'r') as zObject:
        zObject.extractall(path=folder_loc)


    print('Extraction Complete '+folder_loc) 

    files = glob(folder_loc+"ERS Terminal\\*")

    for f in files:
        move(f,folder_loc) 

    rmdir(folder_loc+"ERS Terminal\\")

    setting = open(folder_loc+"setup\\setting.txt",'r')
    VERSION_NUM = setting.read().splitlines()[0]
    setting.close()

    setting_new = open(folder_loc+"setup\\setting.txt",'w')
    setting_new.write(VERSION_NUM+"\n")
    setting_new.write(prev)
    setting_new.close()

    desktop = winshell.desktop()
    print(desktop)
    shortcut_path = path.join(desktop,'ERS Terminal '+VERSION_NUM+'.lnk')
    target = folder_loc+"ERS Terminal "+VERSION_NUM+".exe"
    rename(folder_loc+"ERS Terminal.exe",target)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.IconLocation = folder_loc+"\\setup\\icon.ico"
    shortcut.save()
    print("Shortcut created on Desktop")
    print("Setup Complete")

#?Initial Setup Failed-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def initial_failed(): # if the initial setup has failed, the original directories must be re-initialized (PURGE THEM)

    print("\n--Initial Setup has failed--")
    old_set = open(folder_loc+"setup\\setting.txt",'r')
    old = old_set.read().splitlines()

    print("Saving predefined user settings")
    #saves the users pervious settings 
    prev_version = old[0]
    prev_setting = old[1]

    old_set.close()

    #delete the Desktop shortcut from the previous version
    print("Removing desktop shortcut for Previous Version: "+prev_version)
    remove(winshell.desktop()+'\\ERS Terminal '+prev_version+'.lnk')
    print("Shortcut Removed")

    #remove all the old directories and clear C:\Users\Public\ERS Stackpole\
    #remove the raw data export folder
    print("\nRemoving Raw Data Directory")
    rmdir(folder_loc+"setup\\Raw Data")
    print("Raw Data Directory Removed")
    
    #remove setup folder
    setup_files = glob(folder_loc+"setup\\**")
    print("\nRemoving Setup files")
    for s in setup_files:
        remove(s) #remove one-by-one all the files within setup folder
    print("Setup files removed")
    print("Setup Directory Removed")
    rmdir(folder_loc+"setup") 

    #remove ERS Stackpole Folder
    print("\nRemoving Main Directory Files")
    main_files = glob(folder_loc+"**")

    for m in main_files:
        remove(m) # remove all folders within main dir
    print("Main Directory Files Removed")
    rmdir(folder_loc)
    print("Previous Version Files have been removed and reset")
    print("\n--Installing New Updates--")
    setup(prev_setting) # recalls the setup folder and sends the old setting to save in new file

setup('30') # try initial setup with defaul setting of 30
