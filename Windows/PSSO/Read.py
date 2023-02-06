import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
from copy import deepcopy


# RESULTS += [idSI, nameI == T[idMinJ], elapsed]
if __name__ == '__main__':
    for ID_RUN in [6]:
        P = 40
        LQB = ["QB"] 
        LC =  [ "PSSV16"]
        for nEmb in LC:
            for nQBI in LQB:
                RESULTS = []
                for pId in range(P):
                    inputFile = "R2/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
                    with open(inputFile, "rb") as f:
                        RESULTS += pickle.load(f)
                ACC = []
                T = []
                for i in range(1,len(RESULTS), 3):
                    ACC += [RESULTS[i]]
                    T += [RESULTS[i+1]]
                S = sum(ACC)
                T = sum(T)
                print(nEmb, nQBI, S, len(ACC), S/len(ACC), T/len(ACC), T)



"""
PSSV16 QB20K 6876 12076 0.5693938390195429 0.5174805102422562 6249.094641685486
PSSV16 QB40k 13419 24972 0.5373618452666987 0.9719556532340727 24271.676572561264
PSSV16 QB 23036 49423 0.46609877992028004 1.9013199821891513 93968.93747973442
"""