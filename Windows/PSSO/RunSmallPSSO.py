import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
from tqdm import tqdm

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QB", "rb") as f:
    QB = pickle.load(f)

with open("idSToName", "rb") as f:
    idSToName = pickle.load(f)

LQB = [(QB, "QB")]

# SHARED EMBEDS DATA
EMBEDS_DATA = {}
for nEmb in ["PSSV16"]:
    with open("EMBEDS/"+nEmb, "rb") as f:
        EMBEDS_DATA[nEmb] = pickle.load(f)


def distPSS(A,B):
    k  = min(len(A[0]),len(B[0]))
    k2 = min(len(A[1]),len(B[1]))
    return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])


def minRun(pId, maxId, REPO_ID, distF, nEmb, RUN_ID):
    (QBI, nQBI) = LQB[REPO_ID]
    Q = [idS for idS in QBI[0]]
    
    random.shuffle(Q)
    Q = Q[:200]
    B = QBI[1]
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
	RUN_ID = 6
	random.seed( RUN_ID ) # Seed the repository choices
	start = time.time()
	minRun(0, 1, 0, distPSS, "PSSV16", RUN_ID)
	print(RUN_ID, "PSSO", time.time()-start, "s")

