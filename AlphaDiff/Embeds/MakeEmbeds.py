import numpy as np
from Prototype import computeEmbedding
import time

import pickle

def run(OA, OB, folder):
    O0 = OA[0]
    O1 = OA[1]
    O2 = OB[0]
    O3 = OB[1]
    
    Total = O0+O1+O2+O3
    embeds = computeEmbedding(Total)
    
    with open(folder+"/vecById", "wb") as f:
        pickle.dump(embeds,f)
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")

    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    from makeBenchUO import benchmarkUO
    from makeBenchUV import benchmarkUV
    from makeBenchCV import benchmarkCV
    from makeBenchCO import benchmarkCO
                 #
    run(benchmarkCV("V0","V1"),benchmarkCV("V2","V3"),"CV")
    run(benchmarkCO("O0","O1"),benchmarkCO("O2","O3"),"CO")    
    run(benchmarkUV("V0","V1"),benchmarkUV("V2","V3"),"UV")
    #run(benchmarkUO("O0","O1"),benchmarkUO("O2","O3"),"UO")    
    #run(benchmarkBV("V0","V1"),benchmarkBV("V2","V3"),"BV")
    #run(benchmarkBO("O0","O1"),benchmarkBO("O2","O3"),"BO")
