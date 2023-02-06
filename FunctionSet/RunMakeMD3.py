import numpy as np
from Prototype import computeEmbedding

from multiprocessing import Process
import time
import os
import pickle

from scipy.spatial import distance
from scipy import stats

def distanceE(E1,E2):
    return 1 - len(E1[0].intersection(E2[0]))/len(E1[0].union(E2[0]))


def loadEmbeddings(nameXP, OX):
    embedsOX = computeEmbedding(OX) 
    return embedsOX
        
def run(O, nameXP):
    fTotal = loadEmbeddings(nameXP,O)        
    outputFile =  nameXP+"_MD"
    
    MD = {}
    for (idS,path,compilerOption,name, pathJson) in O:
        MD[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2:
                continue
            start = time.time()
            d = distanceE(fTotal[str(idS)], fTotal[str(idS2)])
            elpased = time.time()-start
            MD[idS][idS2] = (name,name2,compilerOption,compilerOption2,d,elpased)    
    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)
    
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
    
    p1 = Process(target=run, args=(allBO(),"BO"))
    p1.start()

    p2 = Process(target=run, args=(allBV(),"BV"))
    p2.start()
   
    p3 = Process(target=run, args=(allUO(),"UO"))
    p3.start()
    p4 = Process(target=run, args=(allUV(),"UV"))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
   

    p5 = Process(target=run, args=(allCV(),"CV"))
    p5.start()
    p6 = Process(target=run, args=(allCO(),"CO"))
    p6.start()
    
    p5.join()
    p6.join()
    


