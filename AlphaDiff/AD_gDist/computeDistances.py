import pickle
import numpy as np
import sys
import random

import time

def computesDistance(E1,E2):
    
    start = time.time()
    intersectionExtern = E1[1].intersection(E2[1])    
    
    embedsF1 = []
    for f in range(len(E1[0])): 
        embedsF1+= [(E1[0][f][0],E1[0][f][1],np.array([int(extern in E1[0][f][2]) for extern in intersectionExtern]))]        
    
    embedsF2 = []
    for f in range(len(E2[0])): 
        embedsF2+= [(E2[0][f][0],E2[0][f][1],np.array([int(extern in E2[0][f][2]) for extern in intersectionExtern]))]        
        
    dTotal = 0
    for (X0,X1,X2) in embedsF1:        
        dMin = None
        for (Y0,Y1,Y2) in embedsF2:
            d = np.linalg.norm(X0-Y0) + np.linalg.norm(X2-Y2) -(0.75**np.linalg.norm(X1-Y1))
            if dMin == None or d < dMin:
                dMin = d        
        dTotal += dMin
    et = time.time() - start
    return dTotal, et

def main():
    args = sys.argv[1:]
    folder = args[0]
    myId = int(args[1])
    maxID = int(args[2])

    with open(folder+"/vecById", 'rb') as f:
        vecById = pickle.load(f)

    #print("START P", myId)
    numberPrograms = len(vecById)

    random.seed(10)
    distances = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    elapsed = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    
    tasks = []
    for t in range(numberPrograms):
        for p in range(numberPrograms):
            if p == t:
                continue
            tasks += [(t,p)]

    random.shuffle(tasks)
    batchSize = int((1/maxID) * len(tasks)) + 1

    startT = batchSize * myId
    if myId == maxID - 1:
        endT = len(tasks)
    else:
        endT = min(len(tasks),batchSize * (myId+1))
    
    
    for i in range(startT, endT):
        if i >= len(tasks):
            break
        t = tasks[i][0]
        p = tasks[i][1]
        d, et = computesDistance(vecById[t],vecById[p])
        distances[t][p] = d
        elapsed[t][p] = et
        
        
    with open(folder+"/results_"+str(myId), 'wb') as f:
        pickle.dump(distances, f)
    with open(folder+"/elapsed_"+str(myId), 'wb') as f:
        pickle.dump(elapsed, f)
    
if __name__ == "__main__":
    main()
