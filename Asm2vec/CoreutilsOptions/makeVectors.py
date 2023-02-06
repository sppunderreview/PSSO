import time
import numpy as np
import pickle


functionsRemoved = {}

with open("functionsToRemoveCoreutils.txt", "r") as f:
    l = f.readline().strip()[1:-1]
    
    t = l.split(", ")
    
    for i in range(len(t)):
        functionsRemoved[t[i]] = True

    
print(len(functionsRemoved))

toDo = [("O0","O1"),("O0","O2"),("O0","O3"),("O1","O2"),("O1","O3"),("O2","O3")]

for O0, O1 in toDo:
    print(O0,O1)
    path = "experiment_C"+O0+O1+"_0.txt"
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

    with open("./C"+O0+O1+"/vecById", 'wb') as f:
        pickle.dump(vecById, f)
    print("functions", totalF)

"""
25514
O0 O1
functions 38386
O0 O2
functions 35538
O0 O3
functions 35477
O1 O2
functions 29976
O1 O3
functions 29915
O2 O3
functions 27067
"""