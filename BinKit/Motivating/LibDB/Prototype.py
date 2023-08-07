import os

from multiprocessing import Process
import time
import pickle

from copy import deepcopy
from random import choice, shuffle

import numpy as np
from numpy.linalg import norm
from math import log2

import scann
import networkx as nx

def computeEDS(repository):
    EDS = {}
    for (DS, idS) in repository:
        if not(DS in EDS):
            with open("A_"+DS,"rb") as f:
                EDS[DS] = pickle.load(f)
    # Normalize so that dot product x,y = cosine similarity x,y
    for DS in EDS:
        for idS in EDS[DS]:
            for f in EDS[DS][idS][2]:
                EDS[DS][idS][2][f] /= norm(EDS[DS][idS][2][f])

    return EDS

def computeWeights(repository, embedsDS):
    tokensInBinaries = {}
    for (DS, idS) in repository:
        for tokenF in set(embedsDS[DS][str(idS)][3]):
            if not(tokenF in tokensInBinaries):
                tokensInBinaries[tokenF] = []
            tokensInBinaries[tokenF] += [ (DS, idS) ]


    weights = {}
    weightPerBinary = {}

    for (DS, idS) in repository:
        if not(DS in weights):
            weights[DS] = {}
            weightPerBinary[DS] = {}

        weights[DS][idS] = {}
        weightPerBinary[DS][idS] = 0

        wBase = embedsDS[DS][str(idS)][4]
        stringsOccs = embedsDS[DS][str(idS)][5]
        sumN = embedsDS[DS][str(idS)][6]

        for s in stringsOccs:
            sidf = wBase[s] * (stringsOccs[s] / sumN) * -log2(len(tokensInBinaries[s])/len(repository))
            weights[DS][idS][s] = sidf
            weightPerBinary[DS][idS] += sidf


    return weights, weightPerBinary



def createEmbedsRepository(repository, target, embedsDS):
    # Repository
    embedsTotal = []
    idEmbToF = {}
    idE = 0

    for (DS, idS) in repository:
        if DS == target[0] and idS == target[1]:
            continue
        for nF in embedsDS[DS][str(idS)][2]:
            embedsTotal += [embedsDS[DS][str(idS)][2][nF]]
            idEmbToF[idE] = (DS, idS, nF)
            idE += 1

    eR = data=np.array(embedsTotal)

    # Target
    embedsT = []
    idEmbTToF = {}
    idE = 0
    DS  = target[0]
    idS = target[1]
    for nF in embedsDS[DS][str(idS)][2]:
        embedsT += [embedsDS[DS][str(idS)][2][nF]]
        idEmbTToF[idE] = (DS, idS, nF)
        idE += 1

    eT = np.array(embedsT)
    return idEmbToF, idEmbTToF, eR, eT

def cosineSimilarity(x,y):
    return np.dot(x,y)

def computeFunctionPairs(DS,idS,DS2,idS2,EDS):
    pairs = {}
    for f in EDS[DS][str(idS)][2]:
        for f2 in EDS[DS2][str(idS2)][2]:
            cosSim = cosineSimilarity(EDS[DS][str(idS)][2][f],EDS[DS2][str(idS2)][2][f2])
            if cosSim > 0.8: # treshold for function pairs
                if not(f in pairs):
                    pairs[f] = ["", 0]
                # select most similar for each function in target
                if pairs[f][1] < cosSim:
                    pairs[f] = [f2, cosSim]
    return pairs

def removeNodes(G, S):
    for x in S:
        it = G.predecessors(x)
        p = next(it, None)
        if p == x:
           p = next(it, None)
        if p == None:
            continue
        nx.contracted_nodes(G, p, x, self_loops=False, copy=False)
    G.remove_edges_from(nx.selfloop_edges(G))

# [functionExportedNames, callGraph, geminiEmbedsS, strings, wDict, nDict, sumN, elapsed]

def computeClosest(idP, maxID, TR, RR, CANDIDATE_TOP_K, EDS, W, WB):
    outputFile = "R_"+str(idP)
    MD = {}

    for XYZ in range(len(TR)):
        if XYZ % maxID != idP:
            continue
        (DS, idS) = TR[XYZ]

        indexR, indexT, eR, eT = createEmbedsRepository(RR, (DS, idS), EDS)
        #searcher = scann.scann_ops_pybind.builder(eR, 100, "dot_product").score_brute_force().build()
        searcher  = scann.scann_ops_pybind.builder(eR, 100, "dot_product").set_n_training_threads(1).score_ah(2, anisotropic_quantization_threshold=0.2).reorder(200).build()

        startCS = time.time()

        # LIST A
        candidatesA =[]
        for (DS2, idS2) in RR:
            if DS == DS2 and idS == idS2:
                continue
            intersectionExportedNamed = len(EDS[DS][str(idS)][0].intersection(EDS[DS2][str(idS2)][0]))
            commonStrings = EDS[DS][str(idS)][3].intersection(EDS[DS2][str(idS2)][3])
            allStrings = len(EDS[DS][str(idS)][3])

            matchedW = sum([W[DS2][idS2][s] for s in commonStrings])
            totalW = WB[DS2][idS2]

            if totalW == 0:
                totalW = 1

            if allStrings == 0:
                allStrings = 1

            if (len(commonStrings)/allStrings > 0.5) or (matchedW/totalW > 0.1) or (intersectionExportedNamed > 20):
                candidatesA += [(DS2, idS2, [])]

        # LIST B
        neighbors, distances = searcher.search_batched(eT)

        occP = {}
        for iT in range(len(neighbors)):
            idT = indexT[iT]
            for iRI in range(100):
                iR = neighbors[iT][iRI]
                idR = indexR[iR]
                if not(idR[0] in occP):
                    occP[idR[0]] = {}
                if not(idR[1] in occP[idR[0]]):
                    occP[idR[0]][idR[1]] = [0, {}]

                occP[idR[0]][idR[1]][0] += 1
                if distances[iT][iRI] > 0.8: # treshold for function pairs
                    if not(idT[2] in occP[idR[0]][idR[1]][1]):
                        occP[idR[0]][idR[1]][1][idT[2]] = ["", 0]
                    # select most similar for each function in target
                    if occP[idR[0]][idR[1]][1][idT[2]][1] < distances[iT][iRI]:
                        occP[idR[0]][idR[1]][1][idT[2]] = [idR[2], distances[iT][iRI]]

        candidatesB = []
        for DS2 in occP:
            for idS2 in occP[DS2]:
                candidatesB += [(DS2, idS2, occP[DS2][idS2])]
        candidatesB.sort(key=lambda x: x[2][0])
        candidatesB.reverse()
        candidatesB = candidatesB[:CANDIDATE_TOP_K]

        # FCG Filter
        finalCandidates = candidatesA + candidatesB

        mostSimilars = []
        bestScore= 0

        for (DS2, idS2, pairsF) in finalCandidates:
            start = time.time()
            if len(pairsF) != 0:
                pairsF = pairsF[1]
            else:
                pairsF = computeFunctionPairs(DS,idS,DS2,idS2,EDS)

            ET = []
            EC = []

            toSelectC = {}
            toRemoveT = {}

            # Label call graph of target by paired functions in candidate
            # list nodes to remove
            # list nodes (paired functions) to keep in candidate call graph
            for v in EDS[DS][str(idS)][1]:
                # isolated nodes are omitted
                if len(EDS[DS][str(idS)][1][v]) == 0:
                    continue

                nV = "12345_R_"+v
                if not(v in pairsF):
                    toRemoveT[nV] = True
                else:
                    nV = pairsF[v][0]
                    toSelectC[nV] = True

                for n in EDS[DS][str(idS)][1][v]:
                    nN = "12345_R_"+n
                    if not(n in pairsF):
                        toRemoveT[nN] = True
                    else:
                        nN = pairsF[n][0]
                        toSelectC[nN] = True
                    ET += [(nV,nN)]
            # list nodes to remove
            toRemoveC = {}
            for v in EDS[DS2][str(idS2)][1]:
                if len(EDS[DS2][str(idS2)][1][v]) == 0:
                    continue
                if not(v in toSelectC):
                    toRemoveC[v] = True
                for n in EDS[DS2][str(idS2)][1][v]:
                    if not(n in toSelectC):
                       toRemoveC[n] = True
                    EC += [(v,n)]

            FCG_T = nx.DiGraph()
            FCG_T.add_edges_from(ET)

            FCG_C = nx.DiGraph()
            FCG_C.add_edges_from(EC)

            removeNodes(FCG_T, toRemoveT)
            removeNodes(FCG_C, toRemoveC)

            similarityScore = len(set(FCG_T.edges()).intersection(FCG_C.edges()))
            elapsed = time.time() - start
            
            if not(DS in MD):
                MD[DS] = {}
            if not(idS in MD[DS]):
                MD[DS][idS] = {}
            if not(DS2 in MD[DS][idS]):
                MD[DS][idS][DS2] = {}
            MD[DS][idS][DS2][idS2] = (similarityScore, elapsed)
        
        elapsedCS = time.time()-startCS
        print(idS, elapsedCS)
    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)

def computeClosests(TR,RR):
    P = 20

    CANDIDATE_TOP_K = max(5,int((len(RR)*200)/25000))
    EDS = computeEDS(TR+RR) # complete features
    W, WB = computeWeights(RR, computeEDS(RR)) # Weights based on repository

    shuffle(TR)

    PL = []
    for idP in range(P):
        p = Process(target=computeClosest, args=(idP,P, TR, RR, CANDIDATE_TOP_K, EDS, W, WB))
        PL += [p]
        p.start()

    for i in range(P):
        PL[i].join()

    MD = {}
    for idP in range(P):
        inputFile = "R_"+str(idP)
        with open(inputFile, 'rb') as f:
            cD = pickle.load(f)
            for DS in cD:
                if not(DS in MD):
                    MD[DS] = {}
                for idS in cD[DS]:
                    if not(idS in MD[DS]):
                        MD[DS][idS] = {}
                    for DS2 in cD[DS][idS]:
                        if not(DS2 in MD[DS][idS]):
                            MD[DS][idS][DS2] = {}
                        for idS2 in cD[DS][idS][DS2]:
                            MD[DS][idS][DS2][idS2] = cD[DS][idS][DS2][idS2]
                        
    for idP in range(P):
        os.remove("R_"+str(idP))

    return MD

