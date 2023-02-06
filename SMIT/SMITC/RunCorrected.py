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

def similarity(functionsDataS, graphPPredsS, graphPSuccsS, programsSNE, functionsDataT, graphPPredsT, graphPSuccsT, programsTNE, pS, pT, nameFile):
    return functionCallSimilarity(functionsDataS[str(pS)], graphPPredsS[str(pS)], graphPSuccsS[str(pS)], programsSNE[str(pS)], functionsDataT[str(pT)], graphPPredsT[str(pT)], graphPSuccsT[str(pT)], programsTNE[str(pT)], nameFile)
    
def similarityAll(functionsData, graphPPreds, graphPSuccs, programsNE, pS, pT, nameFile):
    return functionCallSimilarity(functionsData[str(pS)], graphPPreds[str(pS)], graphPSuccs[str(pS)], programsNE[str(pS)], functionsData[str(pT)], graphPPreds[str(pT)], graphPSuccs[str(pT)], programsNE[str(pT)], nameFile)


def run(O, OC, idP, maxID, nameXP,fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal):

    random.seed(10)

    nameFile = nameXP+"_"+str(idP)
    logFime = nameXP+"_"+str(idP)+"_log.txt"

    dones = {}


    for otherId in range(40):
        try:
            with open(nameXP+"_"+str(otherId)+"_log.txt", "r") as f:
                lines = f.readlines()
                for l in lines:
                    t = l[1:-2].replace(",","").split(" ")
                    idS = int(t[1])
                    idS2 = int(t[2])
                    dones[str(idS)+"_"+str(idS2)] = True
        except Exception as e:
            pass

    tasks = []
    for (idS,path,compilerOption,name, pathJson) in O:
        for (idS2,path2,compilerOption2,name2, pathJson2) in OC:
            if idS == idS2 or (str(idS)+"_"+str(idS2) in dones):
                continue
            tasks += [(idS,idS2)]
    for (idS,path,compilerOption,name, pathJson) in OC:
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2 or (str(idS)+"_"+str(idS2) in dones):
                continue
            tasks += [(idS,idS2)]

    random.shuffle(tasks)
    print(len(tasks))

    totalT = 0
    N = 0

    i = 0
    for (idS,idS2) in tasks:
        if i % maxID == idP:
            print("START", idP, idS, idS2)
            S2 = time.time()
            dL = 1 - similarityAll(fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, idS, idS2, nameFile)
            elpased = time.time()-S2
            totalT += elpased
            N += 1

            with open(logFime, "a") as f:
                f.write(str([idP,idS,idS2,dL,elpased, totalT/N, totalT, N])+"\n")
        i += 1
    print("END P", idP)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "/home/?/GBigOptions")
    from makeBenchBO import readAllSamples as allBO
    from correctBenchBO import readToCorrect

    P = 20
    TODO = [(allBO(),readToCorrect(),"BOC")]
    
    
    for (PX,PC,DS) in TODO:
        fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal = loadEverything(PX,PC)
        print("STARTING", DS)
        
        PL = []
        for i in range(P):
            p = Process(target=run, args=(PX,PC,i,P,DS,fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal))
            PL += [p]            
            p.start()
        
        for i in range(P):
            PL[i].join()
