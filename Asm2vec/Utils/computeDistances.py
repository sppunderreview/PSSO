import pickle
import numpy as np
import sys
import random

import time

def computesDistance(vectorsP1,vectorsP2):
    dL = 0
    for v in vectorsP1:
        dLM = 1000
        for v2 in vectorsP2:
            d =  np.linalg.norm(v2[1]-v[1], ord=2)
            if d < dLM:
                dLM = d
        dL += dLM
    return dL

def main():
    args = sys.argv[1:]
    folder = args[0]
    myId = int(args[1])
    maxID = int(args[2])
    numberPrograms = int(args[3])
    
    with open(folder+"vecById", 'rb') as f:
        vecById = pickle.load(f)
    
    
    random.seed(10)
    distances = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    tasks = []
    for t in range(0,numberPrograms,1):
        for p in range(0,numberPrograms,1):
            if p == t:
                continue
            if not(p in vecById and t in vecById):
                continue
            if distances[t][p] == 0 :
                tasks += [(t,p)]
                distances[t][p] = -1
    
    random.shuffle(tasks)
    batchSize = int((1/maxID) * len(tasks)) + 1
    
    startT = batchSize * myId
    if myId == maxID - 1:
        endT = len(tasks)
    else:
        endT = batchSize * (myId+1)
    
    start = time.time()
    for i in range(startT, endT):
        if len(tasks) <= i:
            continue
        t = tasks[i][0]
        p = tasks[i][1]

        distances[t][p] = computesDistance(vecById[t],vecById[p])


    with open(folder+"results_"+str(myId), 'wb') as f:
        pickle.dump(distances, f)
        
if __name__ == "__main__":
    main()
