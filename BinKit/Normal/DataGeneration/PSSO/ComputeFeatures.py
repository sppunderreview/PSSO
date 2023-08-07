import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import networkx as nx 
#from scipy.sparse.linalg.eigen.arpack import eigsh as largest_eigsh
from scipy.sparse.linalg import eigsh as largest_eigsh # scipy 1.8

import time
import pickle
from pathlib import Path

from os.path import isfile

from LoadBase import loadGraphs

def makeGraph(lAdj):
    G = nx.Graph()
    for x in lAdj:
        for y in lAdj[x]:
            if x == y:
                continue
            G.add_edge(x, y)
    return G

def computeTopSpectrum(g):
    k = min(len(g)-1,100)
    M = nx.laplacian_matrix(g).asfptype()    
    try:
        return largest_eigsh(M, k, which='LM', return_eigenvectors=False)
    except Exception:
        ncv =  min(len(g), max(10*k + 1, 20))
        return largest_eigsh(M, k, which='LM', ncv=ncv, return_eigenvectors=False)

def preprocessSpectrum(x):
    x = -np.sort(-x)[:100]
    if len(x) < 100:
        x = np.pad(x, (0, 100-len(x)), 'constant')
    return x/np.linalg.norm(x)

def preprocessEdgesCFG(x):
    x = np.array(x)
    x = -np.sort(-x)
    return x/np.linalg.norm(x)

def computeEmbeddings(toDo):
    startBS = time.time()
    u = 0
    for x in toDo:
        idS = x[0]
        outputFile = "Features/"+idS    
        try:        
            start = time.time()
            elapsedP, _, CallGraph, edgesCFG = loadGraphs([x])
            elapsedP = elapsedP[idS]
            CallGraph = CallGraph[idS]
            edgesCFG = edgesCFG[idS]
            
            # Call Graph spectrum normalized
            CallGraphSpectrum = computeTopSpectrum(makeGraph(CallGraph))            
            CallGraphSpectrum = preprocessSpectrum(CallGraphSpectrum)
            
            # Number of edges in CFGs normalized
            edgesCFG = preprocessEdgesCFG(edgesCFG)
            
            elapsedPreprocessing = time.time() - start + elapsedP
            embedding =  [CallGraphSpectrum, edgesCFG, elapsedPreprocessing]
            print(idS, elapsedPreprocessing)

            with open(outputFile, "wb") as f:
                pickle.dump(embedding, f)
        except Exception as err:
            print("Exception:", idS, err)
            #with open(outputFile, "w") as f:
            #    pass

        u += 1
        if u % 100 == 0:            
            timeLeft = ((len(toDo) - u)/ 100) * (time.time()-startBS)
            print(u*100/len(toDo),"%", int(timeLeft), "s")
            startBS = time.time()

if __name__ == '__main__':
    goodware = []
    for path in Path('../jsons').rglob('*'):
        pathJson = str(path)
        goodware += [pathJson]
    
    toDo = []
    
    for pathJson in goodware:
        idS = pathJson.replace(".tmp.json","").split("/")[-1]
        outputFile = "Features/"+idS
        if isfile(outputFile) == True:
            continue
        toDo += [(idS, "?","?","?", pathJson)]

    print(len(toDo))
    computeEmbeddings(toDo)



