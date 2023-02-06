import numpy as np
import time

from Prototype import extractCallGraphs, functionCallSimilarity

from multiprocessing import Process
import pickle

import random

def loadEverything(O,OC):
    functionsData, graphPPreds, graphPSuccs, programsNE = extractCallGraphs(O)    
    functionsDataC, graphPPredsC, graphPSuccsC, programsCNE = extractCallGraphs(OC)
    functionsData.update(functionsDataC)
    graphPPreds.update(graphPPredsC)
    graphPSuccs.update(graphPSuccsC)
    programsNE.update(programsCNE)    
    return functionsData, graphPPreds, graphPSuccs, programsNE

def similarity(functionsDataS, graphPPredsS, graphPSuccsS, programsSNE, functionsDataT, graphPPredsT, graphPSuccsT, programsTNE, pS, pT):
    return functionCallSimilarity(functionsDataS[str(pS)], graphPPredsS[str(pS)], graphPSuccsS[str(pS)], programsSNE[str(pS)], functionsDataT[str(pT)], graphPPredsT[str(pT)], graphPSuccsT[str(pT)], programsTNE[str(pT)])
    
def similarityAll(functionsData, graphPPreds, graphPSuccs, programsNE, pS, pT):    
    return functionCallSimilarity(functionsData[str(pS)], graphPPreds[str(pS)], graphPSuccs[str(pS)], programsNE[str(pS)], functionsData[str(pT)], graphPPreds[str(pT)], graphPSuccs[str(pT)], programsNE[str(pT)])

def run(O, OC, idP, maxID, nameXP):
    random.seed(10)
    
    outputDistance = nameXP+"/results_"+str(idP)
    outputElapsed = nameXP+"/elapsed_"+str(idP)
    
    fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal = loadEverything(O, OC)

        
    distances = [ [0 for j in range(1000)] for i in range(1000) ]
    elapsed   = [ [0 for j in range(1000)] for i in range(1000) ]
    
    tasks = []    
    for (idS,path,compilerOption,name, pathJson) in O:
        for (idS2,path2,compilerOption2,name2, pathJson2) in OC:
            if idS == idS2:
                continue            
            tasks += [(idS,idS2)]
    for (idS,path,compilerOption,name, pathJson) in OC:
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
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
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    from makeBenchBO import readAllSamples as allBO
    from correctBenchBO import readToCorrect

    P = 40    
    TODO = [(allBO(),readToCorrect(),"BOC")]
    
    
    for (PX,PC,DS) in TODO:
        print("STARTING", DS)
        
        PL = []
        for i in range(P):
            p = Process(target=run, args=(PX,PC,i,P,DS))
            PL += [p]            
            p.start()
        
        for i in range(P):
            PL[i].join()
