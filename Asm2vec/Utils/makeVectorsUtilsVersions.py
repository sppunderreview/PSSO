import time
import numpy as np
import pickle


functionsRemoved = {}

with open("functionsToRemoveUtilsVersions.txt", "r") as f:
    l = f.readline().strip()[1:-1]
    
    t = l.split(", ")
    
    for i in range(len(t)):
        functionsRemoved[t[i]] = True

    
print(len(functionsRemoved))

toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3")]

for O0, O1 in toDo:
    print(O0,O1)
    path = "experiment_U"+O0+O1+"_0.txt"
    vectorsbd = {}
    with open(path, "r") as f:
        EPOCHS = f.readline().strip()
        LR = f.readline().strip()
        RATIOET = f.readline().strip()
        nF = f.readline()
        while nF != "":
            nF = nF.strip()
            v = []
            for j in range(200):
                v+= [float(f.readline().strip())]
            vectorsbd[nF] = np.array(v)
            nF = f.readline()
            
    """globalMin = 1000000
    globalMax = -1000000

    for x in vectorsbd:
        globalMin = min(globalMin, np.amin(vectorsbd[x]))
        globalMax = max(globalMax, np.amax(vectorsbd[x]))

    for x in vectorsbd:
        vectorsbd[x] = (vectorsbd[x] - globalMin)/(globalMax-globalMin)
        vectorsbd[x] = vectorsbd[x] / np.linalg.norm((vectorsbd[x]), ord=1)"""

    totalF = 0
    vecById = {}
    for v in vectorsbd:
        p = int(v.split("_")[0])
        if not(p in vecById):
            vecById[p] = []
        if v in functionsRemoved:
            continue
        vecById[p] += [(v,vectorsbd[v])]
        totalF += 1

    with open("./U"+O0+O1+"/vecById", 'wb') as f:
        pickle.dump(vecById, f)
    print("functions", totalF)


"""
8907
V0 V1
functions 48021
V0 V2
functions 48115
V0 V3
functions 49203
V1 V2
functions 49458
V1 V3
functions 50546
V2 V3
functions 50640
"""