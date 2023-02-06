import pickle

import sys
sys.path.insert(0, "C:\\Users\\?\\Desktop\GCoreutilsVersions")

from makeBenchCV import benchmarkCV

toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3")]

for O0, O1 in toDo:
    print(O0,O1)
    with open("C"+O0+O1+"/results", 'rb') as f:
        distances = pickle.load(f)
        
    O0S,O1S = benchmarkCV(O0,O1)
    
    ACC = []
    for (idS,path,compilerOption,name, pathJson) in O0S:
        minD = 100000000
        closest = ""
        for (idS2,path2,compilerOption2,name2, pathJson2) in O1S:
            dE = distances[idS][idS2]
            if dE < minD:
                minD = dE
                closest = name2 
        ACC += [closest == name]
    print(sum(ACC)/len(ACC))
    
    ACC = []
    for (idS,path,compilerOption,name, pathJson) in O1S:
        minD = 100000000
        closest = ""
        for (idS2,path2,compilerOption2,name2, pathJson2) in O0S:
            dE = distances[idS][idS2]
            if dE < minD:
                minD = dE
                closest = name2 
        ACC += [closest == name]
    print(sum(ACC)/len(ACC))
    
    ACC = []
    OAll = O0S + O1S
    for (idS,path,compilerOption,name, pathJson) in OAll:
        minD = 100000000
        closest = ""
        for (idS2,path2,compilerOption2,name2, pathJson2) in OAll:
            if idS == idS2:
                continue
            dE = distances[idS][idS2]
            if dE < minD:
                minD = dE
                closest = name2 
        ACC += [closest == name]
    print(sum(ACC)/len(ACC))
 
"""
V0 V1
0.7816091954022989
0.7701149425287356
0.022988505747126436
V0 V2
0.4827586206896552
0.4827586206896552
0.0
V0 V3
0.40229885057471265
0.2988505747126437
0.0
V1 V2
0.5517241379310345
0.4482758620689655
0.0
V1 V3
0.41379310344827586
0.3793103448275862
0.0
V2 V3
0.41379310344827586
0.4482758620689655
0.0
"""