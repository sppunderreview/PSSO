import numpy as np
from Prototype import computeEmbedding

import time
import os
import pickle

def distanceSP10(E1,E2):   
    k = min(E1[1],E2[1])
    k2 =  min(E1[-2],E2[-2])
    PA = np.linalg.norm(E1[0][:k] - E2[0][:k])
    PB =  np.linalg.norm(E1[2][:k2] - E2[2][:k2])    
    return PA + PB

def distanceA(E1,E2):
    k = min(E1[1],E2[1])
    PA = np.linalg.norm(E1[0][:k] - E2[0][:k])
    return PA
    
def distanceB(E1,E2):
    k2 =  min(E1[-2],E2[-2])
    PB =  np.linalg.norm(E1[2][:k2] - E2[2][:k2])
    return PB

def minRun(O, fTotal, outputFile,dist):
    MD = {}
    for (idS,path,compilerOption,name, pathJson) in O:
        MD[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2:
                continue
            start = time.time()
            d = dist(fTotal[str(idS)], fTotal[str(idS2)])
            elpased = time.time()-start
            MD[idS][idS2] = (name,name2,compilerOption,compilerOption2,d,elpased)    
    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)
        
def run(O, nameXP):
    with open("A_"+nameXP, "rb") as f:
        fTotal = pickle.load(f)    
    
    if nameXP == "BO":
        with open("A_"+nameXP+"_C", "rb") as f:
            fTotalCorrect = pickle.load(f)
        for x in fTotalCorrect:
            fTotal[x] = fTotalCorrect[x]

    minRun(O, fTotal, "./"+nameXP+"_MD", distanceSP10)
    minRun(O, fTotal, "../simCG/"+nameXP+"_MD", distanceA)
    minRun(O, fTotal, "../simCFG/"+nameXP+"_MD", distanceB)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    
    run(allBO(),"BO")
    run(allBV(),"BV")
    run(allUO(),"UO")
    run(allUV(),"UV")
    run(allCV(),"CV")
    run(allCO(),"CO")
    


