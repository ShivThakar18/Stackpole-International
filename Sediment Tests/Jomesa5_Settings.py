from datetime import date

#* Original Running Directory - where the python program will run from
ORIG_DIR = "N:\\Quality\\Jomesa Python\\"           

#* Results Directory - stores all the reports
DIRECTORY = "N:\\Quality\\Metlab\\Met Lab Reports\\Sediment Tests\\Jomesa results\\"
#!DIRECTORY = "C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\"
            #?  N:\Quality\Metlab\Met Lab Reports\Sediment Tests\Jomesa results\10R140 Components
            #?  C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\

#* Litmus Edge Directory - communicate with LE and Database
LE_DIR = "L:\\ShivDataOutput\\Jomesa\\"

#* Local Archive Folder - archive of all data files
LOCALDATA_ARCHIVE = "C:\\Users\\vrerecich\\Desktop\\Jomesa 4 Testing\\Jomesa Data\\"
            #? "C:\\Users\\Administrator\\Documents\\Jomesa Data Archive\\"

#* Picture Directory - saves reaction limit pictures
PIC_DIR = "N:\\Quality\\Metlab\\Met Lab Reports\\Sediment Tests\\Jomesa results\\Reaction Limit Sediment Test Pictures\\"

#* Current Year
TODAY = date.today()        # get data today
YEAR = TODAY.strftime("%Y") # current year for metlab folder

#* Archive File Location
ARCHIVE_FILE = "C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\" + YEAR+" Archive\\"

