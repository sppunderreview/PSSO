import numpy as np
import networkx as nx 

from multiprocessing import Process
import time
import os

from scipy.sparse.linalg import eigs

import pickle

def spectrum(g):
    nodes  = min(nx.number_of_nodes(g) - 2, 1000)
    if nodes <= 0:
        return np.array([1, 1]).astype(float)
    nodes  = max(nodes,1)
    laplacian = nx.laplacian_matrix(g).astype(float)
    eigenvalues = eigs(laplacian, k=nodes, which='LR', return_eigenvectors=False)
    eigenvalues = eigenvalues.real[::-1]
    eigenvalues = eigenvalues / eigenvalues[0]
    return eigenvalues
    
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
    
def miniRun(nameFolder, idS):
    pathIntput = "./CFG/"+nameFolder+"/" + str(idS)+".dot"
    pathOutput = "./CFG/"+nameFolder+"/" + str(idS)
    if os.path.isfile(pathOutput):
        return
    start = time.time()
    G = loadGraph(pathIntput)
    LaplacianG = spectrum(G)
    elasped = time.time()-start
    print(idS,elasped)
    data = (LaplacianG,elasped)
    with open(pathOutput, "wb") as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    import sys
    
    nameFolder = "BO"
    dataUVOrdered = [64,3,74,38,66,76,10,25,52,58,56,18,29,80,49,24,26,36,37,73,75,60,63,65,47,14,44,42,69,11,1,34,20,33,40,19,21,7,82,45,77,15,51,43,83,81,54,8,70,67,55,71,72,35,16,5,41,78,57,30,12,4,48,0,61,9,23,68,6,62,31,53,17,59,39,79,50,2,22,27,32,28,13,46]
    
    PN = 16

    dataUVOrdered2 = []
    for idS in dataUVOrdered:
        pathOutput = "./CFG/"+nameFolder+"/" + str(idS)
        if os.path.isfile(pathOutput):
            continue
        dataUVOrdered2 += [idS]
    dataUVOrdered = dataUVOrdered2
    
    while len(dataUVOrdered) > 0:
        P = []
        i = 0
        for idS in dataUVOrdered:
            p = Process(target=miniRun, args=(nameFolder,idS))
            p.start()
            P += [p]
            i += 1
            if i == PN:
                break
        for p in P:
            p.join()
        dataUVOrdered = dataUVOrdered[PN:]