import time
import numpy as np
import pickle

listDS = [("functionsToRemoveCoreutilsOptions.txt",416,"CO"),("functionsToRemoveCoreutilsVersions.txt",348,"CV"),("functionsToRemoveBigOptions.txt",84,"BO"),("functionsToRemoveBigVersions.txt",84,"BV"),("functionsToRemoveUtilsVersions.txt",88,"UV"),("functionsToRemoveUtilsOptions.txt",88,"UO")]


for (nameFileRemovedFunctions, numberSamples, nameDirectory) in listDS:
    functionsRemoved = {}

    with open(nameFileRemovedFunctions, "r") as f:
        l = f.readline().strip()[1:-1]
        t = l.split(", ")
        
        for i in range(len(t)):
            nameAsm2vec= t[i]
            t2 = nameAsm2vec.split("_")
            idS = int(t2[0])
            nameAsm2vec = "_".join(t2[1:-1])
            if not(idS in functionsRemoved):
                functionsRemoved[idS] = {}
            functionsRemoved[idS][nameAsm2vec] = True

    with open(nameDirectory+"_vecById","rb") as f:
        vecById = pickle.load(f)
            
    totalFunctions = 0
    removed = 0

    globalMin = 1000000
    globalMax = -1000000

    vecByIdCleaned = {}
    for idS in range(numberSamples):
        vecByIdCleaned[idS] = []
        for nameGemini in vecById[idS]:
            nameAsm2vec = "_".join(nameGemini.split("_")[1:])        
            embeds = vecById[idS][nameGemini]
            if nameAsm2vec in functionsRemoved[idS]:
                removed += 1
                continue
            
            totalFunctions += 1
            vecByIdCleaned[idS] += [(nameAsm2vec, embeds)]
            
            #globalMin = min(globalMin, np.amin(embeds))
            #globalMax = max(globalMax, np.amax(embeds))


    """vecByIdNormalized = {}

    for idS in vecByIdCleaned:
        newL = []
        for (nameAsm2vec, embeds) in vecByIdCleaned[idS]:
            newEmbeds = (embeds - globalMin)/(globalMax-globalMin)
            newEmbeds =  newEmbeds / np.linalg.norm((newEmbeds), ord=1)        
            newL += [(nameAsm2vec, newEmbeds)]
        
        vecByIdNormalized[idS] = newL"""

    with open(nameDirectory+"_vecByIdC", 'wb') as f:
        pickle.dump(vecByIdCleaned, f)
    
    print(nameDirectory)
    print("Removed", removed)    
    print("Functions", totalFunctions)
    #print("Normalization", globalMin, globalMax)
    print()

"""
CO
Removed 24428
Functions 41025
Normalization -5830.675 5185.1367

CV
Removed 17985
Functions 20285
Normalization -5830.675 5185.1367

BO
Removed 16935
Functions 192119
Normalization -25805.137 26949.166

BV
Removed 15050
Functions 138705
Normalization -18039.076 19921.143

UV
Removed 8407
Functions 90259
Normalization -9520.139 9033.539

UO
Removed 8550
Functions 110570
Normalization -10209.997 9033.539
"""