import numpy as np
from LoadBase import loadGraphs

import networkx as nx
from ConvNet import ConvNet

import torch
from tqdm import tqdm

def makeGraph(lAdj):
    G = nx.DiGraph()
    for x in lAdj:
        for y in lAdj[x]:
            if x == y:
                continue
            G.add_edge(x, y)
    return G
    
    
def computeEmbedding(inputs):
    alphaDiff = ConvNet()
    state_dict = torch.load( "cnn_20.pt")
    alphaDiff.load_state_dict(state_dict)
    alphaDiff = alphaDiff.eval()

    programs, ExernsP, graphP, graphFName, functionsData = loadGraphs(inputs)
    pV = {}
    for p in tqdm(programs):
        gP = makeGraph(graphP[p])
                
        fEmbeds = []
        for f in graphP[p]:
            inE  = len(list(gP.in_edges(f)))
            outE = len(list(gP.out_edges(f)))
            
            callsF = set()
            for (idF, nextF) in gP.out_edges(f):
                if nextF in graphFName[p]:
                    callsF.add(graphFName[p][nextF])
            
            asm = functionsData[p][f]
            
            bytes = []
            a = 0
            while a < len(asm):
                b = int(asm[a]+asm[a+1], 16)
                bytes += [b]
                a += 2

            v = [ [144 for i in range(100)] for j in range(100)]
            
            i = 0
            j = 0
            for b in bytes:
                if j == 100:
                    break
                v[j][i] = b
                
                i += 1                
                if i == 100:
                    i = 0
                    j += 1

            tensor = torch.from_numpy(np.array(v)).float().unsqueeze(0).unsqueeze(0)
            function_embedding = alphaDiff(tensor).detach().squeeze(0).numpy()           
            fEmbeds += [(function_embedding,np.array([inE,outE]),callsF)] 
         
        pV[int(p)] =  [fEmbeds, ExernsP[p]]
    return pV


