# ---------------------------------------------------------------------------- #
#                      Equator Gauge File Transfer Program                     #
# ---------------------------------------------------------------------------- #
# ------------------------------ Import Modules ------------------------------ #
from glob import glob
from shutil import move
from time import sleep
# ----------------------------- Define Variables ----------------------------- #
OUT = "C:\\EQUATOR\\"
EQ9879_IN = "P:\\*.RES"
EQ9879_OUT = "EQ_9879 (EQUATOR-2827NORenishaw)"
EQ9875_IN = "T:\\*.RES"
EQ9875_OUT = "eq_9875 (Equator-2104n1)"
EQ9877_IN = "W:\\*.RES"
EQ9877_OUT = "Equator_QCCALC (EQUATOR-2970R9)"
# ----------------------------- Transfer Function ---------------------------- #
def transfer(files):

    for f in files:
        if('P:' in f):
            move(f,OUT+EQ9879_OUT)
        if('T:' in f):
            move(f,OUT+EQ9875_OUT)
        if('W:' in f):
            move(f,OUT+EQ9877_OUT)
        sleep(1)
    return 0
# ------------------------- End of Transfer Function ------------------------- #
# ------------------------------- Read Function ------------------------------ #
def read_folder():

    res_files = []

    p_drive = glob(EQ9879_IN)
    t_drive = glob(EQ9875_IN)
    w_drive = glob(EQ9879_IN)

    res_files.append(p_drive)
    res_files.append(t_drive)
    res_files.append(w_drive)

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