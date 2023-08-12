import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
from copy import deepcopy
import numpy as np

from tqdm import tqdm
#from multiprocessing import Process


def distStrings(X, Y):
    return 1 - len(X.intersection(Y))/len(X.union(Y))

def minRun(pId, Q, B, E, T,  maxId, distF, nEmb, RUN_ID):
    outputFile = "RS/R_"+nEmb+"_"+str(pId)+"_"+str(RUN_ID)
    RESULTS = []

    for i in tqdm(range(len(Q))):
        if i % maxId != pId:
            continue
        idSI = Q[i]
        start = time.time()
        dMin = None
        nameI = T[idSI]
        idsMinJ = []
        for idSJ in B:
            if idSI == idSJ:
                continue
            d = distF(E[idSI],E[idSJ])
            if dMin == None or d < dMin :
                dMin = d
                idsMinJ = [idSJ]
            elif d == dMin:
                idsMinJ += [idSJ]
        idMinJ = random.choice(idsMinJ)
        elapsed = time.time() - start
        RESULTS += [idSI, nameI == T[idMinJ], elapsed]

    with open(outputFile, "wb") as f:
        pickle.dump(RESULTS, f)


if __name__ == '__main__':
	RUN_ID = 4
	with open("LABELS", "rb") as f:
		T = pickle.load(f)

	with open("STRINGS", "rb") as f:
		E = pickle.load(f)
	for idS in E:
		E[idS] = set([m for m in E[idS]])

	random.seed ( RUN_ID )

	Q = [idS for idS in E]
	B = [idS for idS in E]
	print("# of IoT malware", len(Q))
	print("Starting Clone Searches")

	start = time.time()
	minRun(0, Q, B, E, T, 1,  distStrings, "STRINGS", RUN_ID)
	print("StringSet", time.time()-start,"s")
