# Gleason

## Overview
This project was designed tp run along side the Gleason CMM Machine at Stackpole PMDA. A third-party program on the Gleason Machine creates a csv file that will be modified using this python script. The python script reads the latest csv file and extracts specific rows and writes them into a new excel file. The excel file is formatted and printed using the default Windows printer. The program on the Gleason computer automatically archives this csv once the excel file is printed.

## How It Works
1. PATHFILE_GLEASON open and read. Assigns the directory locations for the DEFAULT_PATH and SCRAP_PATH
    * DEFUALT_PATH - csv input file location
    * SCRAP_PATH - excel output file location 
    
2. main() is called
    * Uses an infinite while loop. This program is running in the background at all times
    * Searches DEFAULT_PATH for any csv files using glob
         * Iterate through each file found

3. Within main(), the data from the csv file is read using pandas function read_csv() and transposes the data. 

4. Using pandas iloc function, only certain rows are saved into a new DataFrame and the indicies are renamed to the proper names of the characteristics

5. The DataFrame is written to an excel file and printed to the default Windows Printer

## Setup
1. Make sure Gleason.py and PATHFILE_GLEASON.txt are saved within the same directory. 
2. Update PATHFILE_GLEASON.txt to match your directories

### Python Libraries/Modules Used
* glob
* os
* pandas
* pandas.io.formats.excel

### Execution
Update the batch file with the directory of the python executable and python script using the following format:

![image](https://user-images.githubusercontent.com/94186009/213496436-4b0e0fd5-b09d-4812-99a9-2f641fed12f4.png)

* Make sure to put double quotations for each individual path
* Put a space between each address
