
#* ---------------------------------------------------- Shiv Thakar --------------------------------------------------- #
#* ----------------------------------------------------- Jomesa 5 ----------------------------------------------------- #
#* ------------------------------------------ Stackpole International - PMDA ------------------------------------------ #
#* -------------------------------------------- Quality Engineering Intern -------------------------------------------- #
#! -------------------------------------------------------------------------------------------------------------------- #
#!                                                Import Python Libraries                                               #
#! -------------------------------------------------------------------------------------------------------------------- #
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
from os import remove
from Jomesa5_Settings import PIC_DIR                                    #? import variables from Jomesa5_Settings
#? --------------------------------------------------- Save Pictures -------------------------------------------------- #
def savePictures(report):

    pdf = PdfFileReader(report)                                     # initalize object PdfFileReader passing the report
    pdfWriter = PdfFileWriter()                                     # initalize object PdfFileWriter

    pages = []                                                      # holds all the pages that need to be saved

    if('10R140' in report):                                         # for 10R140 components
        removePage = [0, 4]                                     # holds the page numbers that need to be removed

    if('ZF' in report):
        removePage = [0]

    for i in range(pdf.numPages):                                   # iterate through all pages in PdfFileReader object
        if(i in removePage):                                        # if number from removePage list in i, then skip
            continue

        pages.append(i)                                             # add page to pages list
        
    for page_num in pages:                                          
        pdfWriter.addPage(pdf.getPage(page_num))                    # add pages from pages list to pdfWriter object

    PATH = report[0:report.rfind("_")+1] + "Pictures.pdf"           # new save path, rename from /PATH/{REPORT_NUM}_fullreport.pdf to /PATH/{REPORT_NUM}_Pictures.pdf

    with open(PATH,'wb') as f:                                      # open file for writing in binary
        pdfWriter.write(f)                                          # write file
        print("Pictures Saved to PDF Saved")

    remove(report)                                                  # remove the full report from path
#? ------------------------------------------------- Extract Pictures ------------------------------------------------- #
def extractPictures(): 
    files = glob(PIC_DIR + "**\\*_fullreport.pdf")              # search for files that have "_fullreport.pdf" at the end
    for f in files: 
        savePictures(f)                                         # pass files through savePictures function

extractPictures()