import numpy as np
import networkx as nx 

from multiprocessing import Process
import time
import os

from scipy.sparse.linalg import eigs

import pickle


def loadGraph(path):    
    G = nx.Graph()
    
    with open(path,"r") as f:       
        for l in f.readlines():
            if "\" -> \"" in l:
                tl = l.split("\" -> \"")
                u = tl[0].replace("\"", "").replace("\n","")
                v = tl[1].replace("\"", "").replace("\n","")    
                G.add_edge(u,v)
    return G
    
def run(O,nameXP):
    O0 = O[0]
    O1 = O[1]

    OALL = O0+O1

    for (idS,path,compilerOption,name, pathJson) in OALL:
        pathIntput = "./CFG/"+nameXP[0:2]+"/" + str(idS)+".dot"
        print(name,idS,compilerOption,nx.number_of_nodes(loadGraph(pathIntput)))


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")

    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    
    from makeBenchUO import benchmarkUO
    from makeBenchUV import benchmarkUV

    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    """run(benchmarkUV("V0","V1"),"UV0V1")
    run(benchmarkUV("V2","V3"),"UV2V3")"""
    
    """run(benchmarkUO("O0","O1"),"UO0O1")
    run(benchmarkUO("O2","O3"),"UO2O3")"""
    
    """run(benchmarkBV("V0","V1"),"BV0V1")
    run(benchmarkBV("V2","V3"),"BV2V3")"""
    
    run(benchmarkBO("O0","O1"),"BO0O1")
    run(benchmarkBO("O2","O3"),"BO2O3")