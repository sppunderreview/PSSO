import time
import numpy as np
import pickle

nameFileRemovedFunctions = "functionsToRemoveCoreutilsOptions.txt"
numberSamples = 416
nameDirectory = "CO"

functionsRemoved = {}

with open(nameFileRemovedFunctions, "r") as f:
    l = f.readline().strip()[1:-1]
    t = l.split(", ")
    
    for i in range(len(t)):
        nameAsm2vec= t[i]
        t2 = nameAsm2vec.split("_")
        idS = int(t2[0])
        nameSafe = "_".join(t2[1:-1])
        if not(idS in functionsRemoved):
            functionsRemoved[idS] = {}
        functionsRemoved[idS][nameSafe] = True

totalFunctions = 0
removed = 0

vecById = {}
for idS in range(numberSamples):
    vecById[idS] = []
    
    with open("embeds"+nameDirectory+"/"+str(idS),"rb") as f:
        functionsData = pickle.load(f)
    
    for idF in functionsData:
        nameSafe, embeds = functionsData[idF]
        if nameSafe in functionsRemoved[idS]:
            removed += 1
            continue
        
        totalFunctions += 1
        vecById[idS] += [(nameSafe, embeds)]

with open("./"+nameDirectory+"/vecById", 'wb') as f:
    pickle.dump(vecById, f)


print("Removed", removed)    
print("Functions", totalFunctions)
#print("Normalization", globalMin, globalMax)

"""
Removed 25513
Functions 65454
"""