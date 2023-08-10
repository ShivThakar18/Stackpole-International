from os import rename,path
from glob import glob

DIR = 'N:\\Quality\\Metlab\\Met Lab Reports\\Sediment Tests\\Jomesa results\\'

year = ['2022']

partNames = ['GME T4 Stator','ZF\\ZF BODY','ZF\\ZF INNER','ZF\\ZF OUTER']#,'10R140 Components\\10R140 Body']
locations = ['Staright From Washer', 'Eng Trials', 'Point of Ship']

files = []

for part in partNames:
    for y in year: 
        x = glob("C:\\Users\\vrerecich\\Documents\\Jomesa\\2021\\*.pdf")
        files.extend(x)

space = []

for f in files:

    if(' ' in path.basename(f)):
        space.append(f)

for s in space:

    if('ST ' in path.basename(s)):
        reportName = path.basename(s)
        reportName = reportName.replace("ST ", "ST")
        
        filepath = s[0:s.rfind("\\")]
        print(reportName)
        print(filepath)

        rename(s,filepath+"\\"+reportName)




