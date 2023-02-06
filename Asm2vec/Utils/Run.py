#!/usr/bin/python3

# ? ?
# 2022
# ?

import os
import time

import pickle
import numpy as np

def command(folder, id, maxId, programs):
    return "python3 computeDistances.py "+folder+ " "+str(id)+" "+str(maxId)+" "+str(programs)

toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3"),("O0","O1"),("O0","O2"),("O0","O3"),("O1","O2"),("O1","O3"),("O2","O3")]


for O0, O1 in toDo:
    dir = "./U"+O0+O1+"/"
    start = time.time()
    cores = 80
    jobT = ""
    for idL in range(cores):
        jobT += "("+command(dir, idL, cores, 88)+" ) & " 
    jobT += "wait && touch 0.txt"
    os.system(jobT)
    b = time.time()
    print(b-start)
    start = b



