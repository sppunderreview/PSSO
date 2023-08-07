#!/usr/bin/python3

# Tristan Benoit
# 2022
# These

import os
import time

import pickle
import numpy as np

def command(id, maxId):
    return "python3 computeDistances.py "+str(id)+" "+str(maxId)

start = time.time()
cores = 30
jobT = ""
for idL in range(cores):
	jobT += "(sleep "+str(idL*2)+" && "+command(idL, cores)+" ) & " 
jobT += "wait && touch 0.txt"
os.system(jobT)
b = time.time()
print(b-start)




