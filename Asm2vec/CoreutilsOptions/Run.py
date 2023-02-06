#!/usr/bin/python3

# ? ?
# 2021
# ?

import os
import time

import pickle
import numpy as np

def command(folder, id, maxId, programs):
    return "python3 computeDistances.py "+folder+ " "+str(id)+" "+str(maxId)+" "+str(programs)

toDo = [("O0","O1"),("O0","O2"),("O0","O3"),("O1","O2"),("O1","O3"),("O2","O3")]

for O0, O1 in toDo:
    dir = "./C"+O0+O1+"/"
    start = time.time()
    cores = 40
    jobT = ""
    for idL in range(cores):
        jobT += "(sleep "+str(idL*2)+" && "+command(dir, idL, cores, 104*4)+" ) & " 
    jobT += "wait && touch 0.txt"
    os.system(jobT)
    b = time.time()
    print(b-start)
    start = b


