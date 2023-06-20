
# *-------------------------------------- Shiv Thakar - Quality Engineer Intern -------------------------------------- #
# *--------------------------------------------- Stackpole International --------------------------------------------- #
# *-------------------------------------------------- ERS Terminal --------------------------------------------------- #

# !------------------------------------------------- Import Modules -------------------------------------------------- #
from os import path,stat,startfile,remove
from glob import glob
from tkinter import *
import tkinter.messagebox
from datetime import datetime
import subprocess 
from functools import partial 
from shutil import copy

# !------------------------------------------------ Define Variables ------------------------------------------------- #
REPORT_PATH = 'N:\\Quality\\ERS Part Reports\\'             # HARDCODED LOCATION, THIS IS THE PERMANANT LOCATION OF THIS FILE
SETUP_PATH = 'C:\\Users\\Public\\ERS Stackpole\\setup\\'    # SETUP FOLDER WILL ALWAYS GET CREATED AT THIS LOCATION

# SET LOCATIONS FOR FILES WITHIN SETUP FOLDER
HISTORY_PATH = SETUP_PATH+"history_qe.txt"
NAME_PATH = SETUP_PATH+"ers_names.txt"
SETTING_FILE = SETUP_PATH+"setting.txt"

# HARDCODED SCHEDULE LOCATION, WILL NOT CHANGE
SCH_FILE = "N:\\Quality\\Personal Folders for Quality Staff\\Shiv\\ERS_Report_Database.xlsx"

counter = 0 #* global counter 
BKGND = "#252525" #dark grey ; better color for UI

# !----------------------------------------------- Initalize TK Window ----------------------------------------------- #
limit_file = open(SETTING_FILE,'r') #open setting file
read_file = limit_file.read().splitlines()
VERSION_NUM = read_file[0]        
history_limit = int(read_file[1]) #set global limit variable to the saved setting
limit_file.close()

WINDOW = Tk() #main tk window
WINDOW.title("Enterprise Report Scheduler - Stackpole Terminal "+VERSION_NUM) #window title
WINDOW.geometry("550x350") #set dimensions in pixels
WINDOW.configure(bg = BKGND) #background black 
WINDOW.resizable(False,False) #lock the size of the window

CURRENT = '' #current time 

# !---------------------------------------------------- Functions ---------------------------------------------------- #
def update_ersNames():

    file = open(NAME_PATH,'w')
    
    folder = glob(REPORT_PATH + "**\\")

    for f in folder:
        path = f
        part_info = f.split("\\")[3]

        part_num = part_info.split("_")[0]
        part_name = part_info.split("_")[1]
        
        file.write(path+";"+part_num+";"+part_name+"\n")

    file.close()

def open_folder(folder): #displays the folder using file explorer
    subprocess.Popen(r'explorer /open,'+folder)   

def clock(): #main menu clock
    global CURRENT,WINDOW
    NOW = datetime.now() 
    CURRENT = NOW.strftime("%H:%M:%S") #format time

    clock_label = Label(WINDOW, text = CURRENT, fg = 'white', background=BKGND, font = 'Arial 14').place(x = 453, y = 100)

    WINDOW.after(1000,clock) #repeat funciton after 1 second

def reportType(file): #returns the type of report
    if('.txt' in file): # text files are always raw data files
        return "Raw Data Export"

    elif('.xls' in file): # xls files are always Cpk Reports
        return "Cpk Report"

    elif('.pdf' in file): # pdfs are always Histograms
        return "Histogram"

def blankSpace(string,max): 
    TOTAL = max

    space = ' '

    length = len(string)

    space = space * (TOTAL - length)

    return space

# ?-------------------------------------------------- Setting Menu --------------------------------------------------- #
def save_settings(set,w): #saves settings set by user

    global history_limit,VERSION_NUM

    limit_file = open(SETTING_FILE,'w')
    limit_file.write(VERSION_NUM+"\n")
    limit_file.write(str(set.get()))
    history_limit = set.get()
    w.destroy()
    tkinter.messagebox.showinfo("Setting Saved","History Record Limit has been saved to "+str(history_limit))

def setting_menu(): #settings menu UI

    global history_limit

    setting_win = Tk()
    setting_win.title("Enterprise Report Scheduler - Stackpole Quality Engineer Terminal v1.2") #window title
    setting_win.geometry("200x150") #set dimensions in pixels
    setting_win.configure(bg = BKGND) #background black 
    setting_win.resizable(False,False)
    setting_welcome = Label(setting_win,text="Settings Menu",fg = 'white', background= BKGND, font = 'Arial 14').pack()

    limit_options = [5,10,30,100]
    limit_input= IntVar(setting_win)
    limit_input.set(history_limit)

    limit_label = Label(setting_win,text = "History Records Limit",fg = 'white', background= BKGND,font = 'Arial 10').pack(pady = 10)
    options = OptionMenu(setting_win,limit_input,*limit_options)

    options.config(width = 10)
    options.pack(pady=5)


    save_cmd = partial(save_settings,limit_input,setting_win)

    save_button = Button(setting_win,text='Save Settings', command=save_cmd).pack(pady = 10)

    setting_win.mainloop()

# ?--------------------------------------------------- Search Menu --------------------------------------------------- #
def raw_data_viewer(folder):
    files = glob(folder+"\\*.txt")
    for f in files:
        copy(f,SETUP_PATH+"Raw Data")
    
    open_folder(SETUP_PATH+"Raw Data")

def open_result(selected): 

    try:
        raw_data_folder = glob(SETUP_PATH+"Raw Data\\*")
        if(len(raw_data_folder) > 0):
            for r in raw_data_folder:
                remove(r)
    except:
        pass

    sel = selected.get()

    search_win = Tk()
    search_win.title("ERS Part Search - "+sel)
    search_win.geometry("500x200")
    search_win.configure(bg = BKGND) #background black 
    search_win.resizable(False,False) #lock the size of the window

    welcome_label = Label(search_win,text=sel,fg = 'white', background= BKGND, font = 'Arial 14').pack()

    search = sel.split(" ")[0]
 

    ers_name = open(SETUP_PATH+"ers_names.txt",'r')
    ers_read = ers_name.read().splitlines()
    ers_name.close()

    for ers in ers_read: 

        if(search in ers):
            folder = ers.split(";")[0]


    files = glob(folder+"\\*.xls")
    latest_cpk = max(files,key=path.getmtime)

    cpk = Button(search_win, text="View Latest Cpk Report", command = lambda: startfile(latest_cpk)).pack(pady = 5)

    if(search == '72.1077' or search == '72.7018' or search == '72.9623'):

        files = glob(folder+"\\*.pdf")
        latest_histo = max(files, key=path.getmtime)

        histogram = Button(search_win, text='View Latest Histogram', command=lambda: startfile(latest_histo)).pack(pady = 5)

    raw_data = Button(search_win,text='View Latest Raw Data Export',command=lambda:raw_data_viewer(folder)).pack(pady = 5)

    report_folder = Button(search_win, text="Open Part Folder",command=lambda:open_folder(folder)).pack(pady = 5)

    search_win.mainloop() 

def search_results(p,win):
    partnum = p.get()

    ers_name = open(NAME_PATH, 'r')
    ers_read = ers_name.read().splitlines()
    ers_name.close()
    flag = 0

    results = []

    if(len(partnum) < 2):
        flag = -1
        message = "Search must be greater than 2 characters"

        blank = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank.place(relx=0.5,rely=0.6,anchor=CENTER)
        blank2 = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank2.place(relx=0.5,rely=0.7,anchor=CENTER)

    else:
        for ers in ers_read:
            parse = ers.split(";")

            if(partnum in parse[1] or partnum.upper() in parse[2].upper()):
                flag = 1
                results.append(parse[1] +" "+parse[2])
                message = "Results Found Please Confirm Below"
                
            
    if(flag == 0):
        message = "Invalid Part Number, Try Again"
        

    found_label = Label(win, text=message,fg = 'white', background = BKGND,justify='left',width = 50, font = 'Arial 10')

    found_label.place(relx=0.5,rely=0.5,anchor=CENTER)

    if(flag == 0):
        blank = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank.place(relx=0.5,rely=0.6,anchor=CENTER)

        
        blank2 = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank2.place(relx=0.5,rely=0.71,anchor=CENTER)

    if(flag == 1):
        r = StringVar(win,results[0])

        result_ops = OptionMenu(win,r,*results)

        result_ops.config(width = 30)
        result_ops.place(relx=0.5,rely=0.6,anchor=CENTER)
 
        confirm = Button(win,text="Confirm", command = lambda: open_result(r)).place(relx=0.5,rely=0.71,anchor=CENTER)

def search_menu():
    
    w = Tk()

    w.geometry("500x300")
    w.configure(bg = BKGND) #background black 
    w.resizable(False,False)
    w.title("Enterprise Report Scheduler - Part Search")
    part_welcome = Label(w,text="Part Search",fg = 'white', background= BKGND, font = 'Arial 14').pack()


    part_label = Label(w,text = "Enter part number",fg = 'white', background= BKGND,font = 'Arial 10').pack(pady = 5)

    p = Entry(w)
    p.focus_set()
    p.pack(pady = 10)

    search_button = Button(w,text="Search",command = lambda: search_results(p,w)).pack(pady=3)


    w.mainloop()    

# ?-------------------------------------------------- History Menu --------------------------------------------------- #
def getHistory(): #kind of like a refresh button

    history_qe = open(HISTORY_PATH,'w')
    ers_files = glob(REPORT_PATH +"\\*\\*")
    sorted_files = sorted(ers_files, key= lambda t: -stat(t).st_mtime)

    for i in range(history_limit):
        write_string = sorted_files[i] + ";" +str(path.getmtime(sorted_files[i]))+"\n"
        history_qe.write(write_string)

def overall_history(): 
    getHistory()
    
    '''
    ers_names.txt parsing
        folderpath;partnumber;partname
        i.e. N:\\Quality\\ERS Part Reports\\35.0080_10R140Gear;35.0080;10R140 Gear

    history_qe.txt parsing
        filepath;timestamp
        i.e. N:\\Quality\\ERS Part Reports\\58.9121_9121ClutchPlate\\2022-11-15_CpkReport_58.9121.9121.xls;1668525213.971
    '''

    filepaths = []
    timestamps = []
    partnums = []
    reportTypes = []

    history = open(HISTORY_PATH,'r')
    h_read = history.read().splitlines()
    history.close()

    for h in h_read: 
        h_split = h.split(";")
        filepaths.append(h_split[0])
        timestamps.append(h_split[1])

        reportTypes.append(reportType(h))

    namefile = open(NAME_PATH,'r')
    n_read = namefile.read().splitlines()
    namefile.close()

    for h in h_read: 

        slash = h.rfind("\\")
        trimmed = h[0:slash]

        for n in n_read: 
            if(trimmed in n):
                n_split = n.split(';')
                partnums.append(n_split[1] + " " + n_split[2])

    overall_win = Tk()
    overall_win.title("ERS History - Stackpole Terminal v2.1")
    overall_win.geometry("1000x500")
    overall_win.resizable(False,False)

    x = Scrollbar(overall_win, orient='horizontal')
    y = Scrollbar(overall_win)

    x.pack(side = BOTTOM, fill = X)
    y.pack(side = RIGHT, fill = Y)

    t = Text(overall_win, width = 100, height = 100, wrap = NONE,xscrollcommand=x.set,yscrollcommand=y.set, bg = BKGND,fg = 'white')

    t.config(state=NORMAL)
    t.insert(END,"Part Name"+blankSpace("Part Name",35)+"Type"+blankSpace("Type",20)+"Timestamp"+blankSpace("Timestamp",25)+"Folder Path\n")
    

    for num,type,time,file in zip(partnums,reportTypes,timestamps,filepaths):

        time_new = datetime.fromtimestamp(float(time)).isoformat()
        time_new_split = time_new.split("T")
        time_formatted = time_new_split[0] + "  " +time_new_split[1]
        time_final_format = time_formatted.split(".")[0]

        string = num+blankSpace(num,35)+type+blankSpace(type,20)+str(time_final_format)+blankSpace(str(time_final_format),25)+file

        t.insert(END,string+"\n")

        """maybe v2
         open_cmd = partial(open_folder,file)

        open_button.append(Button(overall_win,text='Open', padx = 5, pady = 2, cursor = 'left_ptr',command= lambda text=string: open_folder(file)))
        t.window_create("end-2c", window = open_button[i]) """

    t.pack(side = TOP, fill = X)
    x.config(command = t.xview)
    y.config(command = t.yview)
    t.config(state=DISABLED) #lock text box (no editing can occur)
    overall_win.mainloop()  

def part_history(selected): 
    
    sel = selected.get()
    path_ers = ""

    ers_name = open(NAME_PATH, 'r')
    ers_read = ers_name.read().splitlines()
    ers_name.close()

    for ers in ers_read:

        split_ers = ers.split(";")

        if(split_ers[1] + " " + split_ers[2] == sel):
            path_ers = split_ers[0]

    files = glob(path_ers + "\\*")

    timestamps = []
    reportTypes = []

    sorted_files = sorted(files,key = lambda t: -stat(t).st_mtime)

    for file in sorted_files: 
        reportTypes.append(reportType(file))

        time_new = datetime.fromtimestamp(path.getmtime(file)).isoformat()
        time_new_split = time_new.split("T")
        time_formatted = time_new_split[0] + "  " +time_new_split[1]
        
        timestamps.append(time_formatted.split(".")[0])


    part_hist_win = Tk()
    part_hist_win.title("ERS History - "+sel)
    part_hist_win.geometry("1000x500")
    part_hist_win.resizable(False,False)

    x = Scrollbar(part_hist_win, orient='horizontal')
    y = Scrollbar(part_hist_win)

    x.pack(side = BOTTOM, fill = X)
    y.pack(side = RIGHT, fill = Y)

    t = Text(part_hist_win, width = 100, height = 100, wrap = NONE,xscrollcommand=x.set,yscrollcommand=y.set, bg = BKGND,fg = 'white')
    t.config(state=NORMAL)
    t.insert(END,"Part Name"+blankSpace("Part Name",35)+"Type"+blankSpace("Type",20)+"Timestamp"+blankSpace("Timestamp",25)+"Folder Path\n")
    
    for type,time,file_path,i in zip(reportTypes,timestamps,sorted_files,range(history_limit)):
    
        string = sel+blankSpace(sel,35)+type+blankSpace(type,20)+time+blankSpace(time,25)+file_path
        t.insert(END,string+"\n")

        if(i == history_limit):
            break
    
    t.pack(side = TOP, fill = X)
    x.config(command = t.xview)
    y.config(command = t.yview)
    t.config(state=DISABLED) #lock text box (no editing can occur)

    part_hist_win.mainloop()

def search_part_history(p,win): 

    partnum = p.get()

    ers_name = open(NAME_PATH, 'r')
    ers_read = ers_name.read().splitlines()
    ers_name.close()
    flag = 0

    results = []

    if(len(partnum) < 2):
        flag = -1
        message = "Search must be greater than 2 characters"

        blank = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank.place(relx=0.5,rely=0.6,anchor=CENTER)
        blank2 = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank2.place(relx=0.5,rely=0.7,anchor=CENTER)

    else:
        for ers in ers_read:
            parse = ers.split(";")

            if(partnum in parse[1] or partnum.upper() in parse[2].upper()):
                flag = 1
                results.append(parse[1] +" "+parse[2])
                message = "Results Found Please Confirm Below"
                
            
    if(flag == 0):
        message = "Invalid Part Number, Try Again"
        

    found_label = Label(win, text=message,fg = 'white', background = BKGND,justify='left',width = 50, font = 'Arial 10')

    found_label.place(relx=0.5,rely=0.5,anchor=CENTER)

    if(flag == 0):
        blank = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank.place(relx=0.5,rely=0.6,anchor=CENTER)

        
        blank2 = Label(win,text=" ",background = BKGND,justify='left',width = 40,height= 2)
        blank2.place(relx=0.5,rely=0.71,anchor=CENTER)

    if(flag == 1):
        r = StringVar(win,results[0])

        result_ops = OptionMenu(win,r,*results)

        result_ops.config(width = 30)
        result_ops.place(relx=0.5,rely=0.6,anchor=CENTER)
 
        confirm = Button(win,text="Confirm", command = lambda: part_history(r)).place(relx=0.5,rely=0.71,anchor=CENTER)
 
def byPart_history():

    w = Tk()

    w.geometry("500x300")
    w.configure(bg = BKGND) #background black 
    w.resizable(False,False)
    w.title("Enterprise Report Scheduler - Part History")
    part_welcome = Label(w,text="Part History",fg = 'white', background= BKGND, font = 'Arial 14').pack()


    part_label = Label(w,text = "Enter part number",fg = 'white', background= BKGND,font = 'Arial 10').pack(pady = 5)

    p = Entry(w)
    p.focus_set()
    p.pack(pady = 10)

    search_button = Button(w,text="Search",command = lambda: search_part_history(p,w)).pack(pady=3)


    w.mainloop()
    
def history_menu(): #history menu UI

    '''
    ers_names.txt parsing
        folderpath;partnumber;partname
        i.e. N:\\Quality\\ERS Part Reports\\35.0080_10R140Gear;35.0080;10R140 Gear

    history_qe.txt parsing
        filepath;timestamp
        i.e. N:\\Quality\\ERS Part Reports\\58.9121_9121ClutchPlate\\2022-11-15_CpkReport_58.9121.9121.xls;1668525213.971
    '''

    history_win = Tk()
    history_win.title("Enterprise Report Scheduler - Report History") #window title
    history_win.geometry("200x150") #set dimensions in pixels
    history_win.configure(bg = BKGND) #background black 
    history_win.resizable(False,False)

    history_welcome = Label(history_win,text="Report History",fg = 'white', background= BKGND, font = 'Arial 14').pack()

    overall_button = Button(history_win,text='Overall History',command=overall_history).pack(pady=10)

    byPart_button = Button(history_win,text='History By Part',command=byPart_history).pack(pady=10)

    history_win.mainloop()


    return 0

# !----------------------------------------------- Main User Interface ----------------------------------------------- #
update_ersNames()
welcome_label = Label(WINDOW,text="Welcome to Enterprise Report Scheduler Quality Dashboard",fg = 'white', background= BKGND, font = 'Arial 14').pack()

ers_cmd = partial(open_folder,REPORT_PATH)
ers_folder_button = Button(WINDOW, text="Open ERS Report Folder",font='12',command=ers_cmd).pack(anchor=W,padx = 10,pady = 15) 

search_button = Button(WINDOW, text="Report Search",font='12',command=search_menu).pack(anchor=W,padx = 10,pady=10) 

history_button = Button(WINDOW, text="View Report History",font='12',command=history_menu).pack(anchor=W,padx = 10,pady=10) 

sch_button = Button(WINDOW, text="Open Schedule",font='12',command=lambda: startfile(SCH_FILE)).pack(anchor=W,padx = 10,pady=10)

icon = PhotoImage(file=SETUP_PATH+"settings_icon.png")
icon_sample = icon.subsample(22,22)
settings_button = Button(WINDOW, text="Settings",font='12',image = icon_sample, compound= LEFT,command=setting_menu).pack(anchor=W,padx = 10,pady=10)

logo = PhotoImage(file=SETUP_PATH+"stackpole.png") # stackpole logo
logo_sample = logo.subsample(2,2)
logo_label = Label(WINDOW, image=logo_sample)
logo_label.place(x = 280, y = 40)

clock()

WINDOW.mainloop()  #window mainloop