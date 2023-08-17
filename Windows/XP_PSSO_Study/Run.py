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

LQB = [(QB, "QB")]

# SHARED EMBEDS DATA
EMBEDS_DATA = {}
for nEmb in ["PSSO_30","PSSO_50","PSSO_80","PSSO_130","PSSO_150","PSSO_180"]:
    with open("EMBEDS/"+nEmb, "rb") as f:
        EMBEDS_DATA[nEmb] = pickle.load(f)

def distPSSO(A,B):
    k2 = min(len(A[1]),len(B[1]))
    return np.linalg.norm(A[0] - B[0])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def minRun(pId, maxId, REPO_ID, distF, nEmb, RUN_ID):
    (QBI, nQBI) = LQB[REPO_ID]
    Q = [idS for idS in QBI[0]]
    B = QBI[1]
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
    RUN_ID = 6

    LC = [(distPSSO,"PSSO_30"),(distPSSO,"PSSO_50"),(distPSSO,"PSSO_80"),(distPSSO,"PSSO_130"),(distPSSO,"PSSO_150"),(distPSSO,"PSSO_180")]

    for REPO_ID in [0]:
        random.seed( RUN_ID ) # Seed the repository choices

        for (distF, nEmb) in LC:
            print(RUN_ID, nEmb)
            PL = []
            start = time.time()
            for pId in range(P):
                p = Process(target=minRun, args=(pId, P, REPO_ID, distF, nEmb, RUN_ID))
                PL += [p]
                p.start()

            for p in PL:
                p.join()

            print(RUN_ID, nEmb, time.time()-start, "s")

