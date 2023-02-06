from LoadBase import loadGraphs

import numpy as np
from lapjv import lapjv

def extractCallGraphs(inputs):
    functionsData, graphPPreds, graphPSuccs, programs = loadGraphs(inputs)
    return functionsData, graphPPreds, graphPSuccs, programs

def functionCallSimilarity(functionS, predS, succS, neS, functionT, predT, succT, neT):
    sizeM = len(functionS) + len(functionT)
    matrix = np.zeros((sizeM,sizeM), dtype=np.uint16)
    
    i = 0
    for u in functionS:
        j = 0
        
        outU = len(succS[u])
        inU = len(predS[u])
        
        
        for v in functionT:
            outV = len(succT[v])
            inV = len(predT[v])
            matrix[i][j] = abs(outV - outU) + abs(inV - inU)
            j += 1
        i += 1
        

    i = 0
    for u in functionS:
        outU = len(succS[u])
        inU = len(predS[u])
        matrix[i][i+len(functionT)] = outU + inU + 1
        i += 1

    for i in range(len(functionS)):
        for j in range(len(functionS)):
            if i != j:
                matrix[i][len(functionT) + j] = 10000
    
    i = 0
    for v in functionT:
        outV = len(succT[v])
        inV = len(predT[v])
        matrix[i+len(functionS)][i] = outV + inV + 1
        i += 1
        
    for i in range(len(functionT)):
        for j in range(len(functionT)):
            if i != j:
                matrix[len(functionS)+i][j] = 10000
    
    matrix = np.array(matrix)
    _, _, costTuple = lapjv(matrix)
    (totalCost, _, _) = costTuple
    divisor = sizeM + 2*(neS+neT)
    return 1 - (totalCost/divisor)
