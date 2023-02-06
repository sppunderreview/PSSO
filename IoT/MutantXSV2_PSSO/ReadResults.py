import time
import pickle
import random
import numpy as np
from scipy import stats
from math import sqrt

LC =  ["PSSV16","MUTANTX2"]
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
PSSV16 17206 19959 0.862067237837567 5933.446195602417 0.2972817373416713
MUTANTX2 17357 19953 0.8698942514910039 12863.893474817276 0.644709741633703
"""

# OTHERS

"""
STRINGS 18400 19959 0.9218898742421965 33712.59664773941 1.689092471954477
LIBDX_N 12651 19959 0.6338493912520667 13314.553463935852 0.6670952183945014
LIBDX 14107 19959 0.7067989378225362 28040.173020362854 1.4048886727973773
SHAPE 16329 19959 0.8181271606793927 1285.6691875457764 0.06441551117519798
BSIZE 16353 19959 0.8193296257327521 2874.978763818741 0.14404422886010024
DSIZE 15703 19959 0.7867628638709354 2851.5850546360016 0.14287214062007123
MUTANTX 17340 19953 0.8690422492858216 15792.362949371338 0.7914781210530415
PSS_D_5535 17221 19959 0.8628187784959166 6787.127161502838 0.3400534676838939
SCG_D_5535 15139 19959 0.7585049351169898 3848.043959379196 0.19279743270600713
FUNCTIONSET 12857 19959 0.6441705496267348 466.7781503200531 0.023386850559649938
"""

"""
PREPROCESSING
PSS 0.05018351834058893 1001.6128425598145
SCG 0.05774304969401904 1152.493528842926
PSSV16 0.1418           2830.1862
"""


# TOTAL TIMES

