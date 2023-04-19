# ?------------------------------------------------ Get File Function ------------------------------------------------ #
""" def getFile(): #! UNUSED - checks file source for new files; returns filename

    global LITMUS_DRIVE                                         # global LITMUS_DRIVE variable

    try:
        file = glob(LITMUS_DRIVE + "*.txt")[0]                  # looks for new text files, there should only be 1 at a time
    except:                                                     # except index out of range error when no new files
        print("No New Files")
        return ""                                               # return blank string
    
    print(file) 
    #time = datetime.timestamp(datetime.now())                   # get the current timestamp
    #rename(file,LITMUS_DRIVE+"FollowUp.txt")                    # rename the file with the timestamp at the end

    return LITMUS_DRIVE+"FollowUp.txt"                          # return this new file now """
# ?------------------------------------------------- Parse Timestamp ------------------------------------------------- #
""" def parseTime(file): #! UNUSED - filename parser; returns the timestamp for given file
    
    index = file.rfind(".")                                    # find the index of the last '.' in the filename
    file = file[0:index]                                       # trim the entire file to include everything up to .txt

    return float(((file.split("\\")[-1]).split("_")[-1]))      # split the filename with the delimiters given """
# ?---------------------------------------------------- Copy Data ---------------------------------------------------- #
""" def copyData(SRC,DEST): #! UNUSED - copies the data from the source file to the dest file

    src = open(SRC,'r')                                         # open source file for reading
    copy_to = src.read().splitlines()                           # read and split each line without \n at the end
    src.close()                                                 # close source file

    dest = open(DEST,'w')                                       # open dest file for appending

    for c in copy_to:                                           # iterate through the source file list
        dest.write(c)                                           # write each line to the master file
    dest.close()                                                # close the dest file """
# ?---------------------------------------------------- Move File ---------------------------------------------------- #
""" def movefile(new): #! UNUSED - moves the file to the data folder

    global MASTER, DATA_FOLDER                                  # global variables

    new_time = parseTime(new)                                   # get the timestamp for the new file, call parseTime() function
    MASTER_time = parseTime(MASTER)                             # get the timestamp for the MASTER file, call parseTime() function

    new_file = DATA_FOLDER + path.basename(new)                 # new file needs a new path since it will be moved 
    copy(new,DATA_FOLDER)                                       # move the new file to the data folder
    copyData(new_file,MASTER)                                   # copy data to master, call copyData() function
    remove(new_file)  """                                           # remove the file from the directory
# ?------------------------------------------------- Refresh Master -------------------------------------------------- #
""" def refresh(): #! UNUSED - clears the MASTER file every 2 days

    global MASTER                                               # global MASTER variable
    MASTER = glob(DATA_FOLDER + "MASTER_*.txt")[0]              # use glob to find the text files with the following criteria

    master_time = parseTime(MASTER)                             # get time; use parseTime() function
    now = datetime.timestamp(datetime.now())                    # get the current timestamp

    diff = abs(float(now) - float(master_time))                 # find the difference between both timestamps

    diff = datetime.fromtimestamp(diff)                         # convert to datetime format
                                                                # this will return a date from 1970
                                                                # the timestamp at 0 is equal to Jan 1st 1970 at midnight
                                                                # the timestamp is every second after that date/time
    days = int(diff.strftime("%d"))                             # convert to time

    if(days >= 3):                                              # if the time difference is 3 days
        m = open(MASTER,'r')                                    # open the master file for reading
        m_read = m.read().splitlines()                          # read each line
        m.close()                                               # close the master file

        temp = []                                               # temp list that holds incomplete follow up actions
        for mr in m_read:                                       # iterate through each line
            if(mr[-1] == "0"):                                  # if incomplete, append to temp list
                temp.append(mr)
        
        m = open(MASTER,'w')                                    # open master file for writing
        for t in temp:                                          # iterate through temp list
            m.write(t+"\n")                                     # write each line to file with \n at the end
        m.close()                                               # close master file

        temp_name = DATA_FOLDER + "MASTER_"+str(datetime.timestamp(datetime.now()))+".txt"    
                                                                # give new name to master with new timestamp
        rename(MASTER,temp_name)                                # rename master file
        MASTER = temp_name                                      # set the file
    else:                                                       # if less than 3 days
        print("MASTER Up To Date")  """                   