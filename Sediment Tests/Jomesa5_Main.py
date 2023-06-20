"""
!JOMESA 5.0 
?This program is a simplified and feature expanded version of JOMESA 3.2
?Program will only extract data from the Metlab Report:
    * Date of Analysis
    * Sample Location (Washer, Point of Ship, Eng Trials)
    * Weight
    * Occupancy 
    * All Specs JK, HI, FG, CE
    * Pass/Fail Report

? Once the program has extracted the data, it will be PDF will be updated with pictures only if failed, s
?Updates/Changes: 
    * Remove QC-CALC Compatibility
    * Add Grafana Database Support
    * Add Litmus Edge (Node Red) Compatibility
    * Simplify Program Code
    * Remove Spec Validation (Will be done through Litmus Edge)
    * Encapsulation with Multiple Files and Functions
"""
#* ---------------------------------------------------- Shiv Thakar --------------------------------------------------- #
#* ----------------------------------------------------- Jomesa 5 ----------------------------------------------------- #
#* ------------------------------------------ Stackpole International - PMDA ------------------------------------------ #
#* -------------------------------------------- Quality Engineering Intern -------------------------------------------- #
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                Import Python Libraries                                               #
#! -------------------------------------------------------------------------------------------------------------------- #
from Jomesa5_10R140 import search10R140, get10R140Data       #? import functions from Jomesa_10R140.py
from Jomesa5_ZF import searchZF, getZFData
from Jomesa5_Settings import ORIG_DIR                       #? import variable from Jomesa5_Settings.py
from Jomesa5_Pictures import extractPictures                 #? import functions from Jomesa_Pictures.py
#! ---------------------------------------------- Define Global Variables --------------------------------------------- #
PRINT_FLAG = 0
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                       Functions                                                      #
#! -------------------------------------------------------------------------------------------------------------------- #
#? --------------------------------------------------- Main Function -------------------------------------------------- #
def main():
    global PRINT_FLAG

    while(True):
    
        FILES = []
        if(PRINT_FLAG == 0):
            print("IDLE: Waiting for Files")    # IDLE Message
            PRINT_FLAG = 1                      # set PRINT_FLAG to 1

        FILES.extend(search10R140())            # search files and add to FILES list
        FILES.extend(searchZF())
        
        if(len(FILES) > 0):                     # file found
            for file in FILES:                  # iterate through all files
                print("FILE: " +file)
                if('10R140' in file):
                    get10R140Data(file)         # pass file to the function to get data
                if('ZF' in file):
                    getZFData(file)

            PRINT_FLAG = 0
        
        extractPictures()                       # check if pictures need to be extracted

        break #! Testing ONLY
#! --------------------------------------------------- Function Call -------------------------------------------------- #
main()
