import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np

from multiprocessing import Process
from tqdm import tqdm

# SHARED EMBEDS DATA
EMBEDS_DATA = {}
for nEmb in  ["simCG", "simCFG"]:
    with open("EMBEDS/"+nEmb, "rb") as f:
        EMBEDS_DATA[nEmb] = pickle.load(f)

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QBs", "rb") as f:
    QBs = pickle.load(f)
with open("QBAs", "rb") as f:
    for X in pickle.load(f):
        QBs += [X]

with open("T", "rb") as f:
    idSToName = pickle.load(f)


def distSimCG(A,B):
    k  = min(len(A[0]),len(B[0]))
    return np.linalg.norm(A[0][:k] - B[0][:k])

def distSimCFG(A,B):
    k2 = min(len(A[1]),len(B[1]))
    return np.linalg.norm(A[1][:k2] - B[1][:k2])

def minRun(pId, maxId, QB, distF, nEmb, RUN_ID):
    (nQBI, Q, B)  = QB
    nQBI = nQBI.replace("/", "_VS_")
    E = EMBEDS_DATA[nEmb]
    T = idSToName

    outputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(RUN_ID)
    RESULTS = []

    for i in range(len(Q)):
        if i % maxId != pId:
            continue
        idSI = Q[i]
        if not(idSI in E):
            continue
        start = time.time()
        dMin = None
        nameI = T[idSI]
        idsMinJ = []
        for idSJ in B:
            if idSI == idSJ:
                continue
            if not(idSJ in E):
                continue
            d = distF(E[idSI],E[idSJ])
            if dMin == None or d < dMin :
                dMin = d
                idsMinJ = [idSJ]
            elif d == dMin:
                idsMinJ += [idSJ]

        finalT =  T[random.choice(idsMinJ)]
        elapsed = time.time() - start
        RESULTS += [idSI, nameI == finalT, elapsed]

    with open(outputFile, "wb") as f:
        pickle.dump(RESULTS, f)

if __name__ == '__main__':
    P = 40
    RUN_ID = 1
    LC  = [(distSimCG, "simCG"),(distSimCFG, "simCFG")]

    for QB in QBs:
        random.seed( RUN_ID )
        for (distF, nEmb) in LC:
            PL = []
            start = time.time()
            for pId in range(P):
                p = Process(target=minRun, args=(pId, P, QB, distF, nEmb, RUN_ID))
                PL += [p]
                p.start()

            for p in PL:
                p.join()

            print(QB[0], RUN_ID, nEmb, time.time()-start, "s")


