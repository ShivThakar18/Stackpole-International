
# *--------------------------------------------------- Shiv Thakar --------------------------------------------------- #
# *--------------------------------------------- Stackpole International --------------------------------------------- #
# *--------------------------------------- Equator Gauge File Transfer Program --------------------------------------- #
# *----------------------------------------------- Feburary 8th, 2023 ------------------------------------------------ #
# !------------------------------------------------- Import Modules -------------------------------------------------- #
from glob import glob                                               # file directories
from shutil import move                                             # move files
from time import sleep                                              # time delay
# !------------------------------------------------ Define Variables ------------------------------------------------- #
OUT = "C:\\EQUATOR"                                                 # output folder/QC-Calc Folder
EQ9879_IN = "P:\\*.RES"                                             # P:\ drive for EQ 9879
EQ9875_IN = "T:\\*.RES"                                             # T:\ drive for EQ 9875
EQ9877_IN = "W:\\*.RES"                                             # W:\ drive for EQ 9877
# !---------------------------------------------------- Functions ---------------------------------------------------- #
# ?------------------------------------------------ Transfer Function ------------------------------------------------ #
def transfer(files): #* move files from drive to output folder
    for f in files:                                                 # iterate through files in list
        try:                                                        # error sometimes occurs 
            move(f,OUT)                                             # move each file in the list to the output folder
            print("FILE MOVED - ",f)                
        except:
            print("ERROR RAISED AND EXCEPTED")
        sleep(1)                                                    # wait 1 second
# ?-------------------------------------------------- Read Function -------------------------------------------------- #
def read_folder():  #* reads files from each drive

    res_files = []                                                  # list of files

    p_drive = glob(EQ9879_IN)                                       # files from P:\
    t_drive = glob(EQ9875_IN)                                       # files from T:\
    w_drive = glob(EQ9877_IN)                                       # files from W:\

    for p in p_drive:                                               # append P:\ files to res_files list
        res_files.append(p)
    for t in t_drive:                                               # append T:\ files to res_files list
        res_files.append(t)
    for w in w_drive:                                               # append W:\ files to res_files list
        res_files.append(w)
    transfer(res_files)                                             # call transfer function
# !-------------------------------------------------- Function Call -------------------------------------------------- #
while(True): #* run infinitely
    read_folder()                                                   # call read_folder
    sleep(5)                                                        # wait 5 seconds after one cycle
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                  End of Program                                                    #
# !------------------------------------------------------------------------------------------------------------------- #