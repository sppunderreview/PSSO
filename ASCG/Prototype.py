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

def spectrumD(g1):
    laplacian1 = nx.spectrum.laplacian_spectrum(g1)
    laplacian1 = laplacian1[::-1]
    laplacian1 = laplacian1 / laplacian1[0]
    return laplacian1

def computeEmbedding(inputs):
    elapsedP, programs, graphP,  functionName = loadGraphs(inputs)
    pV = {}
    for p in programs:
        start = time.time()
        gP = makeGraph(graphP[p])
        spectrum = spectrumD(gP)
        elapsed = time.time()-start + elapsedP[p]
        pV[p] = [spectrum, elapsed]
    return pV
