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
    
    nameFolder = "BV"
    dataUVOrdered = [34,68,39,71,81,9,38,57,45,47,58,64,14,44,6,42,36,16,69,67,80,82,8,10,46,48,61,56,15,35,2,75,22,50,24,51,20,21,31,62,74,17,12,27,43,52,13,66,40,19,7,26,1,3,54,18,23,76,37,59,78,49,4,5,70,41,65,33,60,53,83,30,28,11,0,79,55,32,72,77,29,73,25,63]
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