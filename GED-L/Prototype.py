from LoadBase import loadGraphs

import numpy as np
from lapjv import lapjv

def extractCallGraphs(inputs):
    functionsData, graphPPreds, graphPSuccs, programs = loadGraphs(inputs)
    return functionsData, graphPPreds, graphPSuccs, programs

def functionCallSimilarity(functionS, predS, succS, neS, functionT, predT, succT, neT):
    sizeM = len(functionS) + len(functionT)
    
    matrix = [ [0 for j in range(sizeM)] for i in range(sizeM)]
    i = 0
    for u in functionS:
        j = 0
        extU = functionS[u]["externalCalls"]

        for v in functionT:
            extV = functionT[v]["externalCalls"]
            matrix[i][j] = len(extU) + len(extV)  - 2 * len(extU.intersection(extV))
            j += 1
        i += 1
        

    i = 0
    for u in functionS:
        extU = len(functionS[u]["externalCalls"])
        matrix[i][i+len(functionT)] = extU + 1
        i += 1

    for i in range(len(functionS)):
        for j in range(len(functionS)):
            if i != j:
                matrix[i][len(functionT) + j] = 1000
    
    i = 0
    for v in functionT:
        extV = len(functionT[v]["externalCalls"])
        matrix[i+len(functionS)][i] = extV + 1
        i += 1
        
    for i in range(len(functionT)):
        for j in range(len(functionT)):
            if i != j:
                matrix[len(functionS)+i][j] = 1000
    
    
    matrix = np.array(matrix)
    _, _, costTuple = lapjv(matrix)
    (totalCost, _, _) = costTuple
    divisor = sizeM + 2*(neS+neT)
    return 1 - (totalCost/divisor)
