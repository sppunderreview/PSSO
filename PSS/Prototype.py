import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import networkx as nx 
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
    return -np.sort(-nx.spectrum.laplacian_spectrum(g1))

def computeEmbedding(inputs):    
    elapsedP, programs, graphP,  programsSpectrum = loadGraphs(inputs)
    pV = {}
    for p in programs:
        start = time.time()
        gP = makeGraph(graphP[p])
        SL = spectralL(gP)
        
        edgesCFG = []        
        for l in programsSpectrum[p]:
            edgesCFG += [l]            

        SL = SL/np.linalg.norm(SL)

        edgesCFG.sort(reverse=True)
        edgesCFG = np.array(edgesCFG)
        edgesCFG = edgesCFG/np.linalg.norm(edgesCFG)
        
        elapsed = time.time()-start + elapsedP[p]
        print(elapsed,p)
        pV[p] =  [SL, len(SL), edgesCFG, len(edgesCFG),elapsed]
    return pV
