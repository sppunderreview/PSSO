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
    
    nameFolder = "UV"
    dataUVOrdered = [85,63,19,34,75,38,53,37,9,71,24,49,67,45,4,41,47,69,6,43,66,44,3,73,78,79,82,86,83,40,77,84,76,1,81,0,35,27,32,22,28,26,33,31,25,23,29,70,30,68,17,20,7,13,16,12,11,18,8,14,10,39,15,42,5,72,48,46,2,50,59,51,64,55,62,54,57,60,56,61,21,74,80,87,36,52,58,65]
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