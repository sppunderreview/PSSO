#!/usr/bin/python3

# ? ?
# 2022
# ?

import os
import time

import pickle
import numpy as np

def command(folder, id, maxId):
    return "python3 computeDistances.py "+folder+ " "+str(id)+" "+str(maxId)

toDo = ["BO"]

for dir in toDo:
    start = time.time()
    cores = 40
    jobT = ""
    for idL in range(cores):
        jobT += "("+command(dir, idL, cores)+" ) & "
    jobT += "wait && touch 0.txt"
    os.system(jobT)
    b = time.time()
    print("END")
    print(b-start)
    start = b



