import numpy as np
from Prototype import distanceSP16, distanceA, distanceB

import time
import os
import pickle

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

    minRun(O, fTotal, "./"+nameXP+"_MD", distanceSP16)
    #minRun(O, fTotal, "../spectralA/"+nameXP+"_MD", distanceA)
    #minRun(O, fTotal, "../spectralB/"+nameXP+"_MD", distanceB)

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
    


