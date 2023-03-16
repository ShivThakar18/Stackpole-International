# Equator Transfer Program
## Program Description
This program was developed to gather several data files from different network drives to a central folder. 

## Libraries 
- glob
- shutil
- time

## How It Works
At Stackpole we used 3 Renishaw Equator Gauges to conduct measurments and inspections for Clutch Hubs. Each Equator Gauges shares SPC Data on a network drive that another PC has access. 

This program is used to automatically transfer new data files to the QC-Calc Communication Folder. QC-Calc is used for data storage and analysis. 

1. The program reads the 3 network drives (P,T,W) using glob.glob
2. Save each individual list as a bigger list (res_files)
3. Call transfer function with res_files as the arguments
4. Transfer function iterates through the list and moves each file to the QC-Calc Communication folder using shutil.move