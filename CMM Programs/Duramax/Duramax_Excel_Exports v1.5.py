
# *------------------------------------ Shiv Thakar - Quality Engineering Intern ------------------------------------- #
# *--------------------------------------------- Stackpole International --------------------------------------------- #
# *--------------------------------------------- Duramax Excel Exporter ---------------------------------------------- #
# *--------------------------------------------------- Version 1.5 --------------------------------------------------- #
# *------------------------------------------------- March 3rd, 2023 ------------------------------------------------- #
# !------------------------------------------------------------------------------------------------------------------- #
# !                                               Import Python Modules                                                #
# !------------------------------------------------------------------------------------------------------------------- #
from glob import glob
from pandas import read_table,read_csv, DataFrame, ExcelWriter
from os import path, startfile
from shutil import move,copy
from time import sleep
from dataclasses import make_dataclass
from datetime import datetime
# !------------------------------------------------------------------------------------------------------------------- #
# !                                              Define Global Variables                                               #
# !------------------------------------------------------------------------------------------------------------------- #
DEFAULT_PATH = "C:\\Job\\Python\\Duramax_Excel_Export_v2.0\\"               # default path
config_file = open(DEFAULT_PATH + "DURAMAX_FILEPATHS.txt",'r')              # directory configuration 
dir = config_file.read().splitlines()                                       # save txt file lines in list

#ZEISS_PATH = dir[1]                                                         # Zeiss File
ZEISS_PATH = "C:\\Program Files (x86)\\Zeiss\\GearNT\\Reporting\\"
QCCALC_PATH = dir[3]                                                        # QC-Calc Location (Archived Data)
TEMPLATE_PATH = DEFAULT_PATH + "Templates\\"                                # Template locations

ARCHIVE_PATH = DEFAULT_PATH+ "Archived Excel Exports\\"                     # Archived Path

# ------------------------------------------ Temporary Variables for TESTING ----------------------------------------- #
""" DEFAULT_PATH = "C:\\Users\\vrerecich\\Desktop\\Duramax_Files\\"
ZEISS_PATH = DEFAULT_PATH + "Dropbox\\"
QCCALC_PATH = DEFAULT_PATH + "Dropbox\\"
TEMPLATE_PATH = DEFAULT_PATH + "Templates\\"
ARCHIVE_PATH = DEFAULT_PATH + "Excel_Export\\" """
# -------------------------------------------------------------------------------------------------------------------- #
LITMUS_PATH = "L:\\ShivDataOutput\\Duramax\\"                               # node red data folder
EMAIL_PATH = "C:\\Job\\Python\\Email Archive\\"                             # email text file location
printFlag = 0                                                               # While loop print flag
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                     Functions                                                      #
# !------------------------------------------------------------------------------------------------------------------- #
# ?------------------------------------------------ Report Generator ------------------------------------------------- #
def reportGenerator(source_file, template_file): #* Awesome Gear Pro function 
    
    global printFlag                                                        # global printFlag variable

    SOURCE = read_table(source_file, sep='\t')                              # SOURCE pandas dataframe from a table
                                                                            # used to parse source/chr file, 
                                                                            # use tabspace as delimiter

    PARTNB = SOURCE.get("partnb")[1]                                        # get second ([1]) element in "partnb" column
    PROGRAM_NAME = SOURCE.get("planid")[1]                                  # get second ([1]) element in "planid" column

    print(PARTNB)
    print(PROGRAM_NAME)

    TEMPLATE = read_csv(template_file)                                      # TEMPLATE pandas dataframe from a csv
    NUM_OF_ROW = TEMPLATE.shape[0]                                          # get the number of rows from the template
    
    def cal_value(func_name, arg_list): # reads the actual value from the SOURCE text file at each of the line numbers given
                                        # by the arg_list, calculate and return the result based on func_name
        result = 0
        arg_val = [SOURCE.at[i, 'actual'] for i in arg_list]                # get the actual values from the source file using the arg_list indicies
                                                                            # for example; [3,6,9], get actual values from rows 3,6,9 and save as list

        if func_name == "AVERAGE":                                          # if the function is AVERAGE
            result = sum(arg_val) / len(arg_val)                            # take the sum of the value list divided by the length

        if func_name == "EQUAL":                                            # if the function is EQUAL
            result = sum(arg_val)                                           # sum the values in the list

        if func_name == "MIN":                                              # if the function is MIN
            result = min(arg_val)                                           # get the min value of the list

        if func_name == "MAX":                                              # if the function is MAX
            result = max(arg_val)                                           # get the max value from the list

        return round(result, 4)                                             # round result to 4 decimal places

    def cal_status(actual_value, usl=100, lsl=-100): # return "NOT OK" if actual value is out of the limits (USL,LSL)
        status = ""
        if actual_value > usl or actual_value < lsl:                        # if the value is outside of the limits
            status = "NOT OK"                                               # return NOT OK, if not return blank 
        return status                                   

    Dimension = make_dataclass("Dimension",
                            [("Label", str), ("Description", str), ("USL", str), ("LSL", str), ("Actual", float),
                                ("Status", str)])                           # create a datackass
    dim_list = []
    out_of_tolerance_list=[]

    for r in range(NUM_OF_ROW):                                             # iterate through all row of the template
        argument = TEMPLATE.loc[r, 'Argument']                              # extract arguments
        upper_limit = TEMPLATE.loc[r, 'USL']                                # extract upper-sided limit
        lower_limit = TEMPLATE.loc[r, 'LSL']                                # extract lower-sided limit
        function_name = TEMPLATE.loc[r, 'Function']                         # extract function
        argument_list = list(map(int, argument.split("-")))                 # split the arguments, cast to int, and make a list
        value = cal_value(function_name, argument_list)                     # get the calculated value
        status = cal_status(value, upper_limit, lower_limit)                # OK\NOT OK
        
        # build a dimension class
        Label = TEMPLATE.loc[r, 'Label']                                    # place extracted values into the template
        Description = TEMPLATE.loc[r, 'Description']
        USL = TEMPLATE.loc[r, 'USL']
        LSL = TEMPLATE.loc[r, 'LSL']
        Actual = value
        Status = status
        d = Dimension(Label, Description, USL, LSL, Actual, Status)         # make dimension class
        dim_list.append(d)  

        if Status=="NOT OK":                                                # if the status is not OK
            out_of_tolerance_list.append(r)
        
    result = DataFrame(dim_list)

    # write the result to a excel file
    saved_file_name = path.basename(source_file)
    saved_file_name = ZEISS_PATH+saved_file_name

    writer = ExcelWriter(saved_file_name+".xlsx")
    result.to_excel(writer, 'Sheet1')
    workbook1 = writer.book
    worksheets = writer.sheets
    worksheet1 = worksheets['Sheet1']
    # Make the description column longer
    worksheet1.set_column("C:C", 25)
    # worksheet1.column_dimensions['C'].width = 35
    format1 = workbook1.add_format({'bold':  True, 'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    format2 = workbook1.add_format({'bold':  True, 'align': 'left', 'valign': 'top', 'text_wrap': False})

    for line_num in out_of_tolerance_list:
        worksheet1.set_row(line_num+1, cell_format=format1)

    text1 = '             '
    text2 = 'Tolerance File is at ' + TEMPLATE_PATH

    text3 = 'Source Data File is at ' + saved_file_name
    worksheet1.write(len(result) + 1, 0, text1)
    worksheet1.write(len(result) + 2, 0, text2)

    text4 = PROGRAM_NAME + "     " + str(PARTNB)

    worksheet1.write(len(result) + 4, 0, text4)
    worksheet1.set_row(len(result) + 4, cell_format=format2)

    text5 = 'This part is OK'
    if len(out_of_tolerance_list) > 0:
        text5 = 'This part is NOT OK'
    worksheet1.write(len(result) + 5, 0, text5)
    worksheet1.set_row(len(result) + 5, cell_format=format2)
    #writer.save()
    writer.close()

    # Print the result from the absolute path
    startfile(path.abspath(saved_file_name+".xlsx"), "print") #prints file to default printer 
    sleep(10) # sleep for 10 seconds
    print("REPORT PRINTED - "+saved_file_name+".xlsx")

    sleep(5)

    try: 
        move(path.abspath(saved_file_name+".xlsx"),ARCHIVE_PATH ) #move saved file to ARCHIVE_PATH
                        #? C:/Users/Public/Documents/Zeiss/ArchivedReports/
                        #? + path.basename(saved_file_name) + ".xlsx"

    except: 
        pass               
        
    sleep(10)
    print("REPORT ARCHIVED TO ArchivedReports Folder")

    printFlag = 0
    return

    return
# ?--------------------------------------------------- Set Process --------------------------------------------------- #
def setTemplate(name): #* sets the process from basename
    p = ['','']

    if('35.4683' in name):                                  # save the part name depending on what is in the basename
        p[0] = '35.4683'
    elif('35.4684' in name):
        p[0] = '35.4684'
    elif('35.4685' in name):
        p[0] = '35.4685'
    elif('35.4686' in name):
        p[0] = '35.4686'
    elif('35.7371' in name):
        p[0] = '35.7371'

    if('Compact' in name):                                  # depending on the basename passed set the process
        p[1] = 'Compact'
    elif('Machining' in name):
        p[1] = 'Machining'
    elif('Final' in name):
        p[1] = 'Final'
    elif('Sinter' in name):
        p[1] = 'Sinter'
    elif('Grinding' in name):
        p[1] = 'Grinding'
    elif('NCR' in name):
        p[1] = 'NCR'

    return p
# ?-------------------------------------------------- Get Chr Files -------------------------------------------------- #
def getFiles(): #* will save the template file location and the chr file

    global ZEISS_PATH, TEMPLATE_PATH, printFlag                             # global variables

    myfileList = []                                                         # list of all part files
    SEARCH_FILE = open(DEFAULT_PATH+'search_criteria.txt','r')
    SEARCH_CRIT = SEARCH_FILE.read().splitlines()
    SEARCH_FILE.close()

    for name in SEARCH_CRIT:
        myfileList.extend(glob(ZEISS_PATH+name))
    
    try:
        latest_file = max(myfileList, key=path.getmtime)                    # save the latest file 

    except:
        return
    
    basename = path.basename(latest_file)                                   # get the basename from the latest file
    
    if('Calypso' in basename):
        return
  
    cache_file = open(DEFAULT_PATH+"cache.txt","r")                         # open the cache file for reading
    
    try:
        last_file = cache_file.read().splitlines()[0]                       # get the last file from cache
        cache_file.close()                                                  # close the file

        if(latest_file == last_file):                                       # if the latest file is the same as the last_file
            return                                                          # skip and return to main loop 
    except:
        pass                                                                # exception raise, pass (if blank)

    part_process = setTemplate(basename)                                    # call setProcess() function to save the process name
    part = part_process[0]                                                  # save the part
    process = part_process[1]                                               # save the process
    template_name = part+"_"+process+"*.csv"                                # template_name is the part_process*.csv

    template_file = glob(TEMPLATE_PATH+template_name)[0]                    # find the template file

    print(template_file)
    TEMPLATE_FILE = template_file                                           # save to global variable
    SOURCE_FILE = latest_file                                               # save the latest file to global variable

    print(SOURCE_FILE)
    print(TEMPLATE_FILE)

    try:
        reportGenerator(SOURCE_FILE,TEMPLATE_FILE)                          # pass source and template to the reportGenerator

    except:
        time = (datetime.now()).strftime("%m-%d-%Y_%H_%M_%S")
        subject = "Duramax Exception Raised - "+time
        message = "Exception raised at Duramax Excel Exporting Program\nSource File - "+SOURCE_FILE+"\nTemplate File - "+TEMPLATE_FILE
        
        text = open(EMAIL_PATH+'email_exception_'+time+'.txt','w')
        text.write(subject+"\n"+message)
        text.close()
        sleep(5)
        copy(EMAIL_PATH+'email_exception_'+time+'.txt',LITMUS_PATH)

        print(subject)
        print(message)
        printFlag = 0

    #*write chr file to cache text file
    cache_file = open(DEFAULT_PATH+"cache.txt","w")                         # open cache file for writing
    cache_file.write(latest_file)                                           # write the newest file to the cache
    cache_file.close()                                                      # close the file

    return
# !------------------------------------------------------------------------------------------------------------------- #
# !                                                   Function Call                                                    #
# !------------------------------------------------------------------------------------------------------------------- #
while(True):
    if(printFlag == 0):
        print("Waiting for chr files...")       
        printFlag = 1

    getFiles()                                  # call getFiles() function


    