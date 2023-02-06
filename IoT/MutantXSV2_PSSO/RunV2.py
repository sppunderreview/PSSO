import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
from copy import deepcopy
import numpy as np

#from tqdm import tqdm
from multiprocessing import Process

def computeWeights(R, E):
    tokensInBinaries = {}
    for idS in R:
        for tokenF in set(E[idS]):
            if not(tokenF in tokensInBinaries):
                tokensInBinaries[tokenF] = []
            tokensInBinaries[tokenF] += [ idS ]

    weights = {}
    weightPerBinary = {}

    for idS in R:
        weights[idS] = {}
        weightPerBinary[idS] = 0

        stringsOccs = {}
        for tokenF in E[idS]:
            if not(tokenF in stringsOccs):
                stringsOccs[tokenF] = 0
            stringsOccs[tokenF] += 1

        total = 0
        for s in stringsOccs:
            total += stringsOccs[s]

        for s in stringsOccs:
            tfidf = (stringsOccs[s] / total) * len(R)
            tfidf /= len(tokensInBinaries[s])
            weights[idS][s] = tfidf
            weightPerBinary[idS] += tfidf

    return weights, weightPerBinary


def preprocessPSS(E):
	E2 = {}
	for idS in E:
		CG  = np.array(E[idS][:5535])
		CFG = np.array(E[idS][5535:])
		sizeCG  = np.argmax(CG==0)
		sizeCFG = np.argmax(CFG==0)
		E2[idS] = (CG,CFG,sizeCG+1,sizeCFG+1)
	return E2

def preprocessSCG(E):
	E2 = {}
	for idS in E:
		CG  = E[idS]
		sizeCG  = np.argmax(CG==0)
		E2[idS] = (CG,sizeCG+1)
	return E2

def computeMatchingMask(S):
    P_Flag = [ 0 for i in range(len(S))]
    N_Flag = [ 0 for i in range(len(S))]

    nP = 0
    nF = 0

    activePF = False
    activeNF = False

    startFP = 0
    startFN = 0

    anchorsP = []

    for i in range(len(S)):
        if S[i]:
            if nP == 0:
                startFP = i
            nP += 1
            nF  = 0

            if activeNF:
                for j in range(startFN, i):
                    N_Flag[j] = 1
            activeNF = False

        else:
            if nF == 0:
                startFN = i
            nF += 1
            nP  = 0

            if activePF:
                for j in range(startFP, i):
                    P_Flag[j] = 1
                anchorsP += [startFP, i-1]
            activePF = False

        if nP == 10:
            activePF = True

        if nF == 10:
            activeNF = True

    if activeNF:
        for j in range(startFN, len(S)):
            P_Flag[j] = 1

    if activePF:
        for j in range(startFP, len(S)):
            N_Flag[j] = 1
        anchorsP += [startFP, i-1]

    logicMask = P_Flag

    for i in anchorsP:
        for j in range(i,-1,-1):
            if N_Flag[j]:
                break
            logicMask[j] = 1

        for j in range(i,len(logicMask)):
            if N_Flag[j]:
                break
            logicMask[j] = 1
    return logicMask

def distLibDX(idS, idS2, E, W, enableFragments):
    featuresidS = set( E[idS] )

    # Compute matching fragments
    S = []
    for s in E[idS2]:
        S += [ int( s in featuresidS  )]

    # Apply logic blocks mask
    if enableFragments:
        mask = computeMatchingMask(S)
        for i in range(len(mask)):
            mask[i] = mask[i] * S[i]
    else:
        mask = S

    # Retrieve string matched
    stringMatched = {}
    for i in range(len(mask)):
        if mask[i]:
            stringMatched[ E[idS2][i] ] = True

    # Compute matching ratio
    (w, weightPerBinary) = W

    ratio = 0
    for s in stringMatched:
        ratio += w[idS2][s]
    if weightPerBinary[idS2]  == 0:
        return 100

    ratio /= weightPerBinary[idS2]
    return 1 - ratio    

def distStrings(X, Y):
    return 1 - len(X.intersection(Y))/len(X.union(Y))

def distPSS(A,B):
	k  = min(A[2],B[2])
	k2 = min(A[3],B[3])
	return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def distPSS16(A,B):
	k  = min(len(A[0]),len(B[0]))
	k2 = min(len(A[1]),len(B[1]))
	return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def distSCG(A,B):
	k  = min(A[1],B[1])
	return np.linalg.norm(A[0][:k] - B[0][:k], ord=1)

def distSHAPE(A,B):
	return 1 - (min(A[0],B[0])*min(A[1],B[1]))/(max(A[0],B[0])*max(A[1],B[1]))

def distEuclid(A,B):
	return np.linalg.norm(A-B)

def distFS(A, B):
    if len(A) + len(B) == 0:
        return 0
    return 1 - len(A.intersection(B))/len(A.union(B))

def distRandom(A,B):
    return random.random()

def minRunLibDX(pId, Q, B, E, T, maxId, distF, nEmb, RUN_ID, enableFragments):
    W = computeWeights(B, E)
        
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
            d = distF(idSI, idSJ, E, W, enableFragments)
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
    LC = [(distPSS16, "PSSV16"),(distEuclid, "MUTANTX2")]
    RUN_ID = 4

    with open("LABELS", "rb") as f:
        T = pickle.load(f)

    for (distF, nEmb) in LC:
        with open("EMBEDS/"+nEmb, "rb") as f:
            E = pickle.load(f)

        if nEmb == "PSS_D_5535":
            E = preprocessPSS(E)
        elif nEmb == "SCG_D_5535":
            E = preprocessSCG(E)
        elif nEmb == "STRINGS":
            for idS in E:
                E[idS] = set([m for m in E[idS]])

        random.seed ( RUN_ID )

        Q = [idS for idS in E]
        B = [idS for idS in E]
        print("#", nEmb, len(Q),len(E))

        P = 40
        PL = []
        print(nEmb)

        start = time.time()
        for pId in range(P):        
            if nEmb == "LIBDX":
                p = Process(target=minRunLibDX, args=(pId, Q, B, E, T, P, distF, nEmb, RUN_ID, True))
                PL += [p]
                p.start()
            elif nEmb == "LIBDX_N":
                p = Process(target=minRunLibDX, args=(pId,Q, B, E, T, P,  distF, nEmb, RUN_ID, False))
                PL += [p]
                p.start()
            else:
                p = Process(target=minRun, args=(pId, Q, B, E, T, P,  distF, nEmb, RUN_ID))
                PL += [p]
                p.start()

        for p in PL:
            p.join()

        print(nEmb, time.time()-start,"s")


