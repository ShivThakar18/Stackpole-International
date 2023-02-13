# ---------------------------------------------------------------------------- #
#                      Equator Gauge File Transfer Program                     #
# ---------------------------------------------------------------------------- #
# ------------------------------ Import Modules ------------------------------ #
from glob import glob
from shutil import move
from time import sleep
# ----------------------------- Define Variables ----------------------------- #
OUT = "C:\\EQUATOR"
EQ9879_IN = "P:\\*.RES"
EQ9879_OUT = "C:\\EQUATOR\\EQ_9879 (EQUATOR-2827N0Renishaw)"
EQ9875_IN = "T:\\*.RES"
EQ9875_OUT = "C:\\EQUATOR\\eq_9875 (Equator-2104n1)"
EQ9877_IN = "W:\\*.RES"
EQ9877_OUT = "C:\\EQUATOR\\Equator_QCCALC (EQUATOR-2970R9)"
# ----------------------------- Transfer Function ---------------------------- #
def transfer(files):

    for f in files:
        #if('P:' in f):
        try:
            move(f,OUT)
            print("FILE MOVED - ",f)
        except:
            print("ERROR RAISED AND EXCEPTED")
            continue
            
        #if('T:' in f):
            #move(f,OUT)
        #if('W:' in f):
            #move(f,OUT)
        sleep(1)
    return 0
# ------------------------- End of Transfer Function ------------------------- #
# ------------------------------- Read Function ------------------------------ #
def read_folder():

    res_files = []

    p_drive = glob(EQ9879_IN)
    t_drive = glob(EQ9875_IN)
    w_drive = glob(EQ9877_IN)

    for p in p_drive:
        res_files.append(p)
    for t in t_drive:
        res_files.append(t)
    for w in w_drive:
        res_files.append(w)
    transfer(res_files)

    return 0
# --------------------------- End of Read Function --------------------------- #
# ------------------------------- Function Call ------------------------------ #
while(True):

    read_folder()
    sleep(5)
# ---------------------------------------------------------------------------- #
#                                End of Program                                #
# ---------------------------------------------------------------------------- #
