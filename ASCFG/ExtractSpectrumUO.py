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
    
    nameFolder = "UO"
    dataUVOrdered = [1,15,38,56,60,42,78,86,59,41,85,46,28,82,23,84,19,63,25,21,87,65,81,22,18,62,48,55,45,51,54,57,44,49,53,50,0,39,31,36,26,32,30,37,47,35,43,29,27,33,2,9,12,16,13,8,3,14,7,4,10,34,24,83,11,20,61,64,68,5,71,76,72,6,75,17,67,73,79,40,66,70,77,58,74,52,80,69]
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