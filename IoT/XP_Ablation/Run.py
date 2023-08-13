import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
from copy import deepcopy
import numpy as np

from multiprocessing import Process

def preprocessSimCG(E):
	E2 = {}
	for idS in E:
		CG  = np.array(E[idS][:5535])
		sizeCG  = np.argmax(CG==0)
		E2[idS] = (CG, sizeCG+1)
	return E2

def preprocessSimCFG(E):
	E2 = {}
	for idS in E:
		CFG = np.array(E[idS][5535:])
		sizeCFG = np.argmax(CFG==0)
		E2[idS] = (CFG, sizeCFG+1)
	return E2

def distAblation(A,B):
	k  = min(A[1],B[1])
	return np.linalg.norm(A[0][:k] - B[0][:k])

def minRun(pId, Q, B, E, T,  maxId, distF, nEmb, RUN_ID):
    outputFile = "R/R_"+nEmb+"_"+str(pId)+"_"+str(RUN_ID)
    RESULTS = []

    for i in range(len(Q)):
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
    LC = [(distAblation, "simCG_D_5535"),(distAblation, "simCFG_D_5535")]
    RUN_ID = 4

    for (distF, nEmb) in LC:
        with open("EMBEDS/"+nEmb, "rb") as f:
            (E,T) = pickle.load(f)

        if nEmb == "simCG_D_5535":
            E = preprocessSimCG(E)
        elif nEmb == "simCFG_D_5535":
            E = preprocessSimCFG(E)

        random.seed ( RUN_ID )

        Q = [idS for idS in E]
        B = [idS for idS in E]
        print("#", nEmb, len(Q),len(E))

        P = 40
        PL = []
        print(nEmb)

        start = time.time()
        for pId in range(P):        
            p = Process(target=minRun, args=(pId, Q, B, E, T, P,  distF, nEmb, RUN_ID))
            PL += [p]
            p.start()

        for p in PL:
            p.join()

        print(nEmb, time.time()-start,"s")


