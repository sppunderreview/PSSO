import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import networkx as nx
from scipy.sparse.linalg.eigen.arpack import eigsh as largest_eigsh
import time

from LoadBase import loadGraphs

def makeGraph(lAdj):
    G = nx.Graph()
    for x in lAdj:
        for y in lAdj[x]:
            if x == y:
                continue
            G.add_edge(x, y)
    return G

def spectralL(g1):
    k = min(len(g1)-1,100)
    M = nx.laplacian_matrix(g1).asfptype()
    return largest_eigsh(M, k, which='LM', return_eigenvectors=False)    

def preprocessSpectral(S):
    S =  -np.sort(-S)[:100]
    if len(S) < 100:
        S = np.pad(S, (0, 100-len(S)), 'constant')
    return S/np.linalg.norm(S)

def preprocessCFG(CFG):
    CFG = -np.sort(-CFG)
    return CFG/np.linalg.norm(CFG)

def computeEmbedding(inputs):
    print("Reading .json")
    elapsedP, programs, graphP,  programsSpectrum = loadGraphs(inputs)
    pV = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:
        p = str(idS)
        start = time.time()

        # Spectrum of undirected graph
        gP = makeGraph(graphP[p])        
        spectrum = preprocessSpectral(spectralL(gP))

        # CFGs size 
        edgesCFG = preprocessCFG(np.array(programsSpectrum[p]))

        elapsed = time.time()-start + elapsedP[p]
        print("Program", name, "with", compilerOption, ", # of local CFG:", len(edgesCFG), ", time:", elapsed, "s")
        pV[p] =  [spectrum, edgesCFG, elapsed]
    return pV
    
def distanceSP16(E1,E2):
    k = min(len(E1[1]),len(E2[1]))
    return np.linalg.norm(E1[0] - E2[0]) + np.linalg.norm(E1[1][:k] - E2[1][:k])

def distanceA(E1,E2):
    return np.linalg.norm(E1[0] - E2[0])
    
def distanceB(E1,E2):
    k = min(len(E1[1]),len(E2[1]))
    return np.linalg.norm(E1[1][:k] - E2[1][:k])
