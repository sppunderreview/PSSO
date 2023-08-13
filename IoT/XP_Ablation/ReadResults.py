import time
import pickle
import random
import numpy as np
from scipy import stats
from math import sqrt

LC =  ["simCG_D_5535","simCFG_D_5535"]
ID_RUN = 4
P = 40
for nEmb in LC:
    RESULTS = []
    for pId in range(P):
        inputFile = "R/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
        with open(inputFile, "rb") as f:
            RESULTS += pickle.load(f)
    ACC = []
    ESC = []
    for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
        ACC += [RESULTS[i+1]]
        ESC += [RESULTS[i+2]]
    S = sum(ACC)
    TSC = sum(ESC)

    print(nEmb, S, len(ACC), S/len(ACC), TSC, TSC/len(ESC))
    

"""
simCG_D_5535 17093 19959 0.8564056315446665 3307.9562451839447 0.16573757428648453
simCFG_D_5535 17089 19959 0.85620522070244 3238.7793521881104 0.16227162443950652
"""
