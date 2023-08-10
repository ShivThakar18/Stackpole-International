
#* ---------------------------------------------------- Shiv Thakar --------------------------------------------------- #
#* ----------------------------------------------------- Jomesa 5 ----------------------------------------------------- #
#* ------------------------------------------ Stackpole International - PMDA ------------------------------------------ #
#* -------------------------------------------- Quality Engineering Intern -------------------------------------------- #
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                Import Python Libraries                                               #
#! -------------------------------------------------------------------------------------------------------------------- #
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
from os import remove,path
from Jomesa5_Settings import PIC_DIR                                   #? import variables from Jomesa5_Settings
from Jomesa5_Settings import DIRECTORY as JOMESA_DIR
#? --------------------------------------------------- Save Pictures -------------------------------------------------- #
def savePictures(report):

    if('10R140 Body' in report):
        PART = '10R140 Body'
    elif('10R140 Slide' in report):
        PART = '10R140 Slide'
    elif('10R140 Rotor' in report):
        PART = '10R140 Rotor'
    elif('10R140 Gear' in report):
        PART = '10R140 Gear'
    elif('10R140 Gear Nitride' in report):
        PART = '10R140 Gear Nitride'
    elif('ZF BODY' in report):
        PART = 'ZF BODY'
    elif('ZF INNER' in report):
        PART = 'ZF INNER'
    elif('ZF OUTER' in report):
        PART = 'ZF OUTER'
    elif('GME T4 Stator' in report):
        PART = 'GME T4 Stator'

    pdf = PdfFileReader(report)                                     # initalize object PdfFileReader passing the report
    pdfWriter = PdfFileWriter()                                     # initalize object PdfFileWriter

    pages = []                                                      # holds all the pages that need to be saved

    removePage = 0

    for i in range(pdf.numPages):                                   # iterate through all pages in PdfFileReader object
        if(i == removePage):                                        # if number from removePage list in i, then skip
            continue

        pages.append(i)                                             # add page to pages list
        
    for page_num in pages:                                          
        pdfWriter.addPage(pdf.getPage(page_num))                    # add pages from pages list to pdfWriter object

    PATH = PIC_DIR+PART+"\\"+path.basename(report)[0:-4]+"_Pictures.pdf"           # new save path, rename from /PATH/{REPORT_NUM}_fullreport.pdf to /PATH/{REPORT_NUM}_Pictures.pdf

    with open(PATH,'wb') as f:                                      # open file for writing in binary
        pdfWriter.write(f)                                          # write file
        print("Pictures Saved to PDF Saved")

#? ------------------------------------------------- Extract Pictures ------------------------------------------------- #
def extractPictures(): 
    files = glob(PIC_DIR + "**\\*_fullreport.pdf")              # search for files that have "_fullreport.pdf" at the end
    for f in files: 
        savePictures(f)                                         # pass files through savePictures function
#? ----------------------------------------------------- Read Log ----------------------------------------------------- #
def readLog():

    LOG_FILE = PIC_DIR+"LOG.txt"                                    # log file holds a list of reports where the pictures need to be saved
                                                                    # reports that have failed or crossed the reaction limit

    FILE = open(LOG_FILE,'r')                     
    log_data = FILE.read().splitlines()
    FILE.close()

    for i in range(len(log_data)):
        log_data[i] = log_data[i].strip()
        log_data[i] = log_data[i].replace('\x00','')
        
    log_data = list(dict.fromkeys(log_data))

    for i in range(len(log_data)):
        report_num = log_data[i].split("\\")[-1]
        for f in list(glob(JOMESA_DIR +  log_data[i][0: log_data[i].rfind("\\")+1]+"*.pdf")):
            if(report_num in f):
                log_data[i] = f
    
    if(len(log_data) > 0):
        for l in log_data:
            print("ACTIVE: Saving pictures for "+l)
            savePictures(l)

    FILE = open(LOG_FILE,'w')
    FILE.close()
readLog()