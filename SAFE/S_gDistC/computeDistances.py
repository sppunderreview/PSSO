import pickle
import numpy as np
import sys
import random
import time

def computesDistance(vectorsP1,vectorsP2):
    start = time.time()
    dL = 0
    for v in vectorsP1:
        dLM = 1000
        for v2 in vectorsP2:
            d =  np.linalg.norm(v2[1]-v[1], ord=2)
            if d < dLM:
                dLM = d
        dL += dLM
    et = time.time() - start
    return dL, et

def main():
    args = sys.argv[1:]
    folder = args[0]
    myId = int(args[1])
    maxID = int(args[2])
    
    
    with open(folder+"/vecById", 'rb') as f:
        vecById = pickle.load(f)

    with open(folder+"C/vecById", 'rb') as f:
        vecByIdC = pickle.load(f)    
    vecById.update(vecByIdC)    
    numberPrograms = len(vecById)
    print(len(vecById))
    random.seed(10)
    distances = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    elapsed = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    tasks = []
    for t in [5,6,12]:
        for p in range(numberPrograms):
            if p == t:
                continue
            if distances[t][p] == 0 :
                tasks += [(t,p)]
                distances[t][p] = -1
    for t in range(numberPrograms):
        for p in [5,6,12]:
            if p == t:
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

    for i in range(startT, endT):
        if i >= len(tasks):
            break
        print("Doing", myId, i)
        t = tasks[i][0]
        p = tasks[i][1]
        if not(p in vecById and t in vecById):
            continue
        d, et = computesDistance(vecById[t],vecById[p])
        distances[t][p] = d
        elapsed[t][p] = et
        print("Done", myId, i, et)


    with open(folder+"C/X_results_"+str(myId), 'wb') as f:
        pickle.dump(distances, f)
    with open(folder+"C/X_elapsed_"+str(myId), 'wb') as f:
        pickle.dump(elapsed, f)

if __name__ == "__main__":
    main()
