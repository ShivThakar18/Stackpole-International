import pandas as pd

FOLDERS = {
    1 : "10R140 Body",
    2 : "10R140 Gear",
    3 : "10R140 Nitride",
    4 : "10R140 Rotor",
    5 : "10R140 Slide",
    6 : "GME Stator",
    7 : "ZF Body",
    8 : "ZF Inner",
    9 : "ZF Outer"
}

FILE_IN = "C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\Jomesa Data.xlsx"
FILE_OUT = "C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\SEND TO DB\\"+FOLDERS[1]+"\\"

COUNTER = 0

dataFrame = pd.read_excel(FILE_IN, sheet_name=FOLDERS[1],header=None)
# test 123
for i in range(len(dataFrame.index)):
    string = ""
    report = dataFrame.iloc[i,1]

    if("GME" in FILE_OUT):
        part = dataFrame.iloc[i,2]
    else:
        part = dataFrame.iloc[i,3]

    COUNTER = COUNTER + 1
    name = FILE_OUT + str(COUNTER) + "_" + str(report) + "_" + str(part) + ".txt"

    for j in range(len(dataFrame.columns)):

        if(str(dataFrame.iloc[i,j]) == "nan"):
            string = string + ","
            continue

        if(j == 0):
            string  = string + str(dataFrame.iloc[i,j])[0:10] + ","
        elif(j == len(dataFrame.columns) - 1 and 'ZF' in FILE_OUT):
            string  = string + str(dataFrame.iloc[i,j]) + ","
        elif(j == len(dataFrame.columns) - 1 and ('10R140' in FILE_OUT or 'GME' in FILE_OUT)):
            string  = string + str(dataFrame.iloc[i,j]) 
        else:
            string  = string + str(dataFrame.iloc[i,j]) + ","   

    text = open(name,"w")
    text.write(string)
    text.close()
    
