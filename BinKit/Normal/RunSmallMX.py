import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
from collections import Counter

from multiprocessing import Process
from tqdm import tqdm


# SHARED EMBEDS DATA
EMBEDS_DATA = {}
for nEmb in  ["MUTANTX2"]:
    with open("EMBEDS/"+nEmb, "rb") as f:
        EMBEDS_DATA[nEmb] = pickle.load(f)

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QBs", "rb") as f:
    QBs = pickle.load(f)
with open("QBAs", "rb") as f:
    QBs += pickle.load(f)

with open("T", "rb") as f:
    idSToName = pickle.load(f)


def distEuclid(A,B):
    return np.linalg.norm(A-B)

def minRun(pId, maxId, QB, distF, nEmb, RUN_ID):
    (nQBI, Q, B)  = QB
    nQBI = nQBI.replace("/", "_VS_")
    E = EMBEDS_DATA[nEmb]
    T = idSToName

    outputFile = "RS/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(RUN_ID)
    RESULTS = []

    for i in tqdm(range(len(Q))):
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
    RUN_ID = 1
    LC  = [(distEuclid, "MUTANTX2")]

    for QB in QBs:
        print(QB[0], len(QB[1]),len(QB[2]))
        random.seed( RUN_ID )
        for (distF, nEmb) in LC:
            start = time.time()
            minRun(0, 1, QB, distF, nEmb, RUN_ID)
            print(QB[0], RUN_ID, nEmb, time.time()-start, "s")
        break
