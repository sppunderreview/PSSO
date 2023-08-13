import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
import pandas as pd

from copy import deepcopy


# RESULTS += [idSI, nameI == T[idMinJ], elapsed]
if __name__ == '__main__':
    for ID_RUN in [3]:
        P = 40
        LQB = ["QB"]
        LC =  ["simCG", "simCFG"]
        #, (distRandom, "Random")]

        for nEmb in LC:
            for nQBI in LQB:
                RESULTS = []
                for pId in range(P):
                    inputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
                    with open(inputFile, "rb") as f:
                        RESULTS += pickle.load(f)
                ACC = []
                T = []
                for i in range(1,len(RESULTS), 3):
                    ACC += [RESULTS[i]]
                    T += [RESULTS[i+1]]
                print(nEmb, nQBI, sum(ACC)/len(ACC), sum(T)/len(T), sum(T))

"""
simCG QB 0.4586695791112999 1.1170988402927833 55232.717960596085
simCFG QB 0.16265194264102098 1.0556707101701193 52195.52692294121
"""
