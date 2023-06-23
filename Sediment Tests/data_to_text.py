import pandas as pd

FILE_IN = "C:\\Users\\vrerecich\\Desktop\\Jomesa Data 10R140.xlsx"
FILE_OUT = "C:\\Users\\vrerecich\\Desktop\\OUT\\ZF Body\\"
COUNTER = 0

dataFrame = pd.read_excel(FILE_IN, sheet_name="ZF Body",header=None)
# test 123
for i in range(len(dataFrame.index)):
    string = ""
    report = dataFrame.iloc[i,1]
    part = dataFrame.iloc[i,3]
    COUNTER = COUNTER + 1
    name = FILE_OUT + str(COUNTER) + "_" + report + "_" + part + ".txt"

    for j in range(len(dataFrame.columns)):

        if(str(dataFrame.iloc[i,j]) == "nan"):
            string = string + ","
            continue

        if(j == 0):
            string  = string + str(dataFrame.iloc[i,j])[0:10] + ","
        elif(j == len(dataFrame.columns) - 1 and 'ZF' in FILE_OUT):
            string  = string + str(dataFrame.iloc[i,j]) + ","
        elif(j == len(dataFrame.columns) - 1 and '10R140' in FILE_OUT):
            string  = string + str(dataFrame.iloc[i,j]) 
        else:
            string  = string + str(dataFrame.iloc[i,j]) + ","   

    text = open(name,"w")
    text.write(string)
    text.close()
    
