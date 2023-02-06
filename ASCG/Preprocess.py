import numpy as np
from Prototype import computeEmbedding

from multiprocessing import Process
import time
import pickle


def run(O, nameXP):
    embedsO = computeEmbedding(O)    
    with open("A_"+nameXP, "wb") as f:
        pickle.dump(embedsO, f)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "/home/?/GBigOptions")
    sys.path.insert(0, "/home/?/GBigVersions")
    sys.path.insert(0, "/home/?/GCoreutilsVersions")
    sys.path.insert(0, "/home/?/GCoreutilsOptions")
    sys.path.insert(0, "/home/?/GUtilsVersions")
    sys.path.insert(0, "/home/?/GUtilsOptions")

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