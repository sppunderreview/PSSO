import numpy as np
import networkx as nx 
import time

from LoadBase import loadGraphs

def makeGraph(lAdj, functionName):
    G = nx.Graph()
    for x in lAdj:
        for y in lAdj[x]:
            if not(y in functionName):
                continue
            nameX = functionName[x]
            nameY = functionName[y]

            if nameX == nameY:
                continue
            #if "sub_" in nameX and "sub_" in nameY:
            G.add_edge(nameX, nameY)
    return G

def spectralRadius(g1):
    laplacian1 = nx.spectrum.laplacian_spectrum(g1)
    laplacian1[::-1].sort()
    laplacian1 = laplacian1 / laplacian1[0]
    return laplacian1

def computeEmbedding(inputs):
    programs, graphP,  functionName = loadGraphs(inputs)
    pV = {}
    for p in programs:
        gP = makeGraph(graphP[p], functionName)
        pV[p] = spectralRadius(gP)
    return pV
