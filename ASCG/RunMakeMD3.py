import numpy as np
from Prototype import computeEmbedding

from multiprocessing import Process
import time
import os
import pickle

from scipy.spatial import distance
from scipy import stats

def distanceE(E1,E2):
    k = min(len(E1[0]),len(E2[0]))
    return np.linalg.norm(E1[0][:k]-E2[0][:k], ord=1)

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
            
    minRun(O, fTotal, nameXP+"_MD", distanceE)
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")

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
    


