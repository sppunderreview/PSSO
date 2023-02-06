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
    
    nameFolder = "CV"
    for idS in range(348):
        miniRun(nameFolder,idS)

