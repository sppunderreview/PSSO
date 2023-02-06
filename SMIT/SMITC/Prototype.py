from LoadBase import loadGraphs

import editdistance
from UnionFind import DisjointSet

from LoadBase import loadGraphs

import numpy as np
import subprocess

import time

mnemonicsEditMemory = {}

def extractCallGraphs(inputs):
    functionsData, graphPPreds, graphPSuccs, programs = loadGraphs(inputs)
    return functionsData, graphPPreds, graphPSuccs, programs

def mnemonicEditDistance(mList1,mList2):
    global mnemonicsEditMemory

    str1 = mList1[1]
    str2 = mList2[1]
    
    if str1 in mnemonicsEditMemory:
        if str2 in mnemonicsEditMemory[str1]:
            return mnemonicsEditMemory[str1][str2]
    
        else:
            mnemonicsEditMemory[str1][str2] = editdistance.eval(mList1[0], mList2[0])
            return mnemonicsEditMemory[str1][str2]

    mnemonicsEditMemory[str1] = {}
    mnemonicsEditMemory[str1][str2] = editdistance.eval(mList1[0], mList2[0])
    return mnemonicsEditMemory[str1][str2]

def cleanMemory():
    global mnemonicsEditMemory
    mnemonicsEditMemory.clear()

def extractExternalFunction(functionD):
    external = []
    for f in functionD:
        if functionD[f]["extern"] == False:
            continue
        external += [f]
    return external

def callSequenceSignature(succs, leaders):
    seq = []
    for u in succs:
        if u in leaders:
            seq += [leaders[u]]
    return seq

def labelsSet(list, atomicFunctions, locals):
    labels = set()
    
    for x in list:
        if x in locals:
            labels.add("local")
        elif x in atomicFunctions.leader:
            labels.add(atomicFunctions.leader[x])
    return labels    


def functionCallSimilarity(functionS, predS, succS, neS, functionT, predT, succT, neT, nameFile):
    # None Atomic Functions
    U_S_V = {}
    for f in functionS:
        U_S_V[f] = True
    U_T_V = {}
    for f in functionT:
        U_T_V[f] = True
    
    # Atomic functions
    atomicFunctions = DisjointSet()

    # Matching external functions
    externalFunctionS = extractExternalFunction(functionS)
    externalFunctionT = extractExternalFunction(functionT)
    for u in externalFunctionS:
        for v in externalFunctionT:
            if functionS[u]["name"] == functionT[v]["name"]:
                atomicFunctions.add(u,v)
                if u in U_S_V:
                    del U_S_V[u]
                if v in U_T_V:
                    del U_T_V[v]
    
    # Matching local functions by edit distance of mnemonic
    
    for uS in functionS:
        for uT in functionT:
            editDistance = mnemonicEditDistance(functionS[uS]["mnemonics"], functionT[uT]["mnemonics"])
            if editDistance * 100 < 15 * min(functionS[uS]["len"], functionT[uT]["len"]):
                atomicFunctions.add(uS,uT)
                if uS in U_S_V:
                    del U_S_V[uS]
                if uT in U_T_V:
                    del U_T_V[uT]
    
    # Matching local functions by the same sequence of calls functions    
    repeat = True
    
    while repeat:
        repeat = False
        for uS in functionS:
            if not(uS in U_S_V):
                continue    
            callSeqSignatureS = callSequenceSignature(succS[uS], atomicFunctions.leader)
            for uT in functionT:
                if not(uT in U_T_V):
                    continue

                callSeqSignatureT = callSequenceSignature(succT[uT], atomicFunctions.leader)

                if callSeqSignatureS == callSeqSignatureT:
                    repeat = True
                    atomicFunctions.add(uS,uT)
                    if uS in U_S_V:
                        del U_S_V[uS]
                    del U_T_V[uT]

    sizeM = len(U_S_V) + len(U_T_V)
    if sizeM == 0:
        return 1
    
    # Cost Matrix
    costMatrix = np.zeros((sizeM,sizeM), dtype=np.uint16)
    i = 0
    for u in U_S_V:
        j = 0
        
        outU = labelsSet(succS[u], atomicFunctions, U_S_V)
        inU = labelsSet(predS[u], atomicFunctions, U_S_V)

        for v in U_T_V:
            outV = labelsSet(succT[v], atomicFunctions, U_T_V)
            inV = labelsSet(predT[v], atomicFunctions, U_T_V)
            costMatrix[i][j] = len(outU) + len(inU) + len(outV) + len(inV) - 2 * ( len(outU.intersection(outV)) + len(inU.intersection(inV)))
            j += 1
        i += 1
        

    i = 0
    for u in U_S_V:
        outU = len(succS[u])
        inU = len(predS[u])
        costMatrix[i][i+len(U_T_V)] = outU + inU + 1
        i += 1

    for i in range(len(U_S_V)):
        for j in range(len(U_S_V)):
            if i != j:
                costMatrix[i][len(U_T_V) + j] = 1000
    
    i = 0
    for v in U_T_V:
        outV = len(succT[v])
        inV = len(predT[v])
        costMatrix[i+len(U_S_V)][i] = outV + inV + 1
        i += 1
        
    for i in range(len(U_T_V)):
        for j in range(len(U_T_V)):
            if i != j:
                costMatrix[len(U_S_V)+i][j] = 1000
    
    

    # Factor of reduction when (i,j) are matched based on mnemonics 
    factorMatrix = np.ones((sizeM,sizeM), dtype=np.single)
    i = 0
    for u in U_S_V:
        j = 0
        
        uM = functionS[u]["mnemonics"]
        for v in U_T_V:
            vM = functionT[v]["mnemonics"]
            factorMatrix[i][j] = min(1, mnemonicEditDistance(uM,vM) / max(len(uM[0]), len(vM[0])))
            j += 1
        i += 1
    
    # Clean mnemonicEditDistance memory
    cleanMemory()
    
    # Adjacency Matrix for S 
    adjacencyS = np.zeros((sizeM,sizeM), dtype=np.bool_)
    
    neSWithoutC = 0
    
    i = 0
    for u in U_S_V:
        j = 0
        for v in U_S_V:            
            if v in succS[u] or u in succS[v]  :
                adjacencyS[i][j] = True
                neSWithoutC += 1
            j += 1
        i += 1

    # Adjacency Matrix for T 
    adjacencyT = np.zeros((sizeM,sizeM), dtype=np.bool_)
    
    neTWithoutC = 0
    
    i = 0
    for u in U_T_V:
        j = 0
        for v in U_T_V:            
            if v in succT[u] or u in succT[v]  :
                adjacencyT[i][j] = True
                neTWithoutC += 1
            j += 1
        i += 1
    
    # Ask C Algorithm NBHA
    nameFile = "/tmp/instance_"+nameFile+".txt"
    with open(nameFile, "w") as f:
        f.write(str(sizeM)+"\n")
        
        for i in range(sizeM):
            for j in range(sizeM):
                f.write(str(costMatrix[i][j]))
                if j+1 < sizeM:
                    f.write(" ")        
            f.write("\n")

        for i in range(sizeM):
            for j in range(sizeM):
                f.write(str(factorMatrix[i][j]))
                if j+1 < sizeM:
                    f.write(" ")        
            f.write("\n")
            
        for i in range(sizeM):
            for j in range(sizeM):
                f.write(str(int(adjacencyS[i][j])))
                if j+1 < sizeM:
                    f.write(" ")        
            f.write("\n")
            
        for i in range(sizeM):
            for j in range(sizeM):
                f.write(str(int(adjacencyT[i][j])))
                if j+1 < sizeM:
                    f.write(" ")        
            f.write("\n")
    
    

    process = subprocess.Popen(["./NBHAE", nameFile], stdout=subprocess.PIPE)
    totalCost = process.communicate()[0].decode("utf-8")
    try:
        totalCost = float(totalCost)
        divisor = sizeM + 2*(neSWithoutC+neTWithoutC)
        return  1 - (totalCost/divisor)
    except Exception as e:
        print(e)
        print(totalCost)
        return 0
