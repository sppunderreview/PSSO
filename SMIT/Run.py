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

def similarity(functionsDataS, graphPPredsS, graphPSuccsS, programsSNE, functionsDataT, graphPPredsT, graphPSuccsT, programsTNE, pS, pT, nameFile):
    return functionCallSimilarity(functionsDataS[str(pS)], graphPPredsS[str(pS)], graphPSuccsS[str(pS)], programsSNE[str(pS)], functionsDataT[str(pT)], graphPPredsT[str(pT)], graphPSuccsT[str(pT)], programsTNE[str(pT)], nameFile)
    
def similarityAll(functionsData, graphPPreds, graphPSuccs, programsNE, pS, pT, nameFile):
    return functionCallSimilarity(functionsData[str(pS)], graphPPreds[str(pS)], graphPSuccs[str(pS)], programsNE[str(pS)], functionsData[str(pT)], graphPPreds[str(pT)], graphPSuccs[str(pT)], programsNE[str(pT)], nameFile)

def run(OA, OB, idP, maxID, nameXP):
    random.seed(10)
    
    logFime = nameXP+"_"+str(idP)+"_log.txt"
    nameFile = nameXP+"_"+str(idP)    
    
    fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, OTotal = loadEverything(OA,OB)

    tasks = []    
    for (idS,path,compilerOption,name, pathJson) in OTotal:
        for (idS2,path2,compilerOption2,name2, pathJson2) in OTotal:
            if idS == idS2:
                continue            
            tasks += [(idS,idS2)]
    
    random.shuffle(tasks)
    random.shuffle(tasks)
    
    totalT = 0
    N = 0    

    i = 0
    for (idS,idS2) in tasks:
        if i % maxID == idP:
            S2 = time.time()
            dL = 1 - similarityAll(fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, idS, idS2, nameFile)
            elpased = time.time()-S2
            totalT += elpased
            N += 1
            
            with open(logFime, "a") as f:
                f.write(str([idP,idS,idS2,dL,elpased, totalT/N, totalT, N])+"\n")
        i += 1


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "/home/?/GCoreutilsVersions")
    sys.path.insert(0, "/home/?/GCoreutilsOptions")
    sys.path.insert(0, "/home/?/GUtilsVersions")
    sys.path.insert(0, "/home/?/GUtilsOptions")

    from makeBenchCV import benchmarkCV    
    from makeBenchCO import benchmarkCO
    
    from makeBenchUV import benchmarkUV    
    from makeBenchUO import benchmarkUO     
    
    P = 30
    
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
