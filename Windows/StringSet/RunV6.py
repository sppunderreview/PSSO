import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np

from multiprocessing import Process

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QB", "rb") as f:
    QB = pickle.load(f)

with open("idSToName", "rb") as f:
    idSToName = pickle.load(f)

# SHARED EMBEDS DATA
EMBEDS_DATA = {}
for nEmb in ["STRINGS"]:
    with open("EMBEDS/"+nEmb, "rb") as f:
        EMBEDS_DATA[nEmb] = pickle.load(f)
    for idS in EMBEDS_DATA[nEmb]:
        EMBEDS_DATA[nEmb][idS] = set(EMBEDS_DATA[nEmb][idS][0])


def distStrings(X, Y):
    return 1 - len(X.intersection(Y))/len(X.union(Y))

def minRun(pId, maxId, distF, nEmb, RUN_ID):
    global QB, idSToName, EMBEDS_DATA 
    QBI = QB
    nQBI = "QB"
    Q = [idS for idS in QBI[0]]
    B = QBI[1]
    E = EMBEDS_DATA[nEmb]
    T = idSToName

    outputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(RUN_ID)
    RESULTS = []

    newI = -1
    finalQ = []
    for i in range(len(Q)):
        if i % 3 != 0:
            continue
        newI += 1
        if newI % maxId != pId:
            continue
        finalQ += [Q[i]]

    print(RUN_ID, pId, nQBI, len(finalQ))

    for idSI in finalQ:
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
    P = 10
    RUN_ID = 3

    LC = [(distStrings, "STRINGS")]
    random.seed( RUN_ID ) # Seed the repository choices

    for (distF, nEmb) in LC:
        PL = []
        start = time.time()
        for pId in range(P):
            p = Process(target=minRun, args=(pId, P, distF, nEmb, RUN_ID))
            PL += [p]
            p.start()

        for p in PL:
            p.join()

        print(RUN_ID, time.time()-start, "s")
