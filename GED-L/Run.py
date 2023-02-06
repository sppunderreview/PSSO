import numpy as np
import time

from Prototype import extractCallGraphs, functionCallSimilarity

from multiprocessing import Process
import pickle

import random

def loadEverything(OA,OB):
    O0 = OA[0]
    O1 = OA[1]    
    O2 = OB[0]
    O3 = OB[1]
        
    functionsDataS, graphPPredsS, graphPSuccsS, programsSNE = extractCallGraphs(O0)
    functionsDataT, graphPPredsT, graphPSuccsT, programsTNE = extractCallGraphs(O1)
    functionsDataU, graphPPredsU, graphPSuccsU, programsUNE = extractCallGraphs(O2)
    functionsDataV, graphPPredsV, graphPSuccsV, programsVNE = extractCallGraphs(O3)
        
    
    OTotal = O0+O1+O2+O3
    
    fDTotal = {**functionsDataS, **functionsDataT, **functionsDataU, **functionsDataV}
    gPPresdTotal = {**graphPPredsS, **graphPPredsT, **graphPPredsU, **graphPPredsV}
    gPSuccsTotal = {**graphPSuccsS, **graphPSuccsT, **graphPSuccsU, **graphPSuccsV}
    pNETotal = {**programsSNE, **programsTNE, **programsUNE, **programsVNE}
    
    return fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, OTotal

def similarity(functionsDataS, graphPPredsS, graphPSuccsS, programsSNE, functionsDataT, graphPPredsT, graphPSuccsT, programsTNE, pS, pT):
    return functionCallSimilarity(functionsDataS[str(pS)], graphPPredsS[str(pS)], graphPSuccsS[str(pS)], programsSNE[str(pS)], functionsDataT[str(pT)], graphPPredsT[str(pT)], graphPSuccsT[str(pT)], programsTNE[str(pT)])
    
def similarityAll(functionsData, graphPPreds, graphPSuccs, programsNE, pS, pT):    
    return functionCallSimilarity(functionsData[str(pS)], graphPPreds[str(pS)], graphPSuccs[str(pS)], programsNE[str(pS)], functionsData[str(pT)], graphPPreds[str(pT)], graphPSuccs[str(pT)], programsNE[str(pT)])

def run(OA, OB, idP, maxID, nameXP):
    random.seed(10)
    
    outputDistance = nameXP+"/results_"+str(idP)
    outputElapsed = nameXP+"/elapsed_"+str(idP)
    
    fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, OTotal = loadEverything(OA,OB)
        
    distances = [ [0 for j in range(1000)] for i in range(1000) ]
    elapsed   = [ [0 for j in range(1000)] for i in range(1000) ]
    
    tasks = []    
    for (idS,path,compilerOption,name, pathJson) in OTotal:
        for (idS2,path2,compilerOption2,name2, pathJson2) in OTotal:
            if idS == idS2:
                continue            
            tasks += [(idS,idS2)]
    
    random.shuffle(tasks)    
    
    i = 0
    for (idS,idS2) in tasks:
        if i % maxID == idP:
            start = time.time()
            distances[idS][idS2] = 1 - similarityAll(fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, idS, idS2)
            el = time.time()-start
            elapsed[idS][idS2] = el
        i += 1

    with open(outputDistance, "wb") as f:
        pickle.dump(distances, f)
        
    with open(outputElapsed, "wb") as f:
        pickle.dump(elapsed, f)

if __name__ == '__main__':
    import sys

    sys.path.insert(0, "/home/?/GCoreutilsVersions")
    sys.path.insert(0, "/home/?/GCoreutilsOptions")    
    sys.path.insert(0, "/home/?/GUtilsVersions")
    sys.path.insert(0, "/home/?/GUtilsOptions")    
    sys.path.insert(0, "/home/?/GBigOptions")
    sys.path.insert(0, "/home/?/GBigVersions")

    from makeBenchCV import benchmarkCV
    from makeBenchCO import benchmarkCO
    from makeBenchUV import benchmarkUV
    from makeBenchUO import benchmarkUO
    from makeBenchBV import benchmarkBV
    from makeBenchBO import benchmarkBO

    P = 40
    
    TODO = [(benchmarkCV("V0","V1"),benchmarkCV("V2","V3"), "CV"),(benchmarkBO("O0","O1"),benchmarkBO("O2","O3"),"BO"),(benchmarkCO("O0","O1"),benchmarkCO("O2","O3"), "CO"),(benchmarkUV("V0","V1"),benchmarkUV("V2","V3"), "UV"),(benchmarkUO("O0","O1"),benchmarkUO("O2","O3"), "UO"),(benchmarkBV("V0","V1"),benchmarkBV("V2","V3"), "BV")]
    
    
    for (P1,P2,DS) in TODO:
        print("STARTING", DS)
        
        PL = []
        for i in range(P):
            p = Process(target=run, args=(P1,P2,i,P,DS))
            PL += [p]            
            p.start()
        
        for i in range(P):
            PL[i].join()
