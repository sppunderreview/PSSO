import json
import networkx as nx 
import time
 
def loadGraphs(inputs):
    elapsedP = {}
    programs = {}
    graphP = {}
    programsSpectrum = {}
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        start = time.time()
        
        with open(pathJson) as f:
          data = json.load(f)
        
        idProgram = str(idS)
        programs[idProgram] = True
        graphP[idProgram] = {}
        programsSpectrum[idProgram] = []

        for f in data["functions"]:
            idFunction = "P_"+idProgram+"F_"+str(f["id"])            
            graphP[idProgram][idFunction] = []
            
            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphP[idProgram][idFunction] += [idNF]
            
            G = nx.Graph()
            isOk = False
            for b in f["blocks"]:
                 idB = b["id"]
                 for nextB in b["call"]:
                    G.add_edge(idB, nextB)
                    isOk = True 
            if isOk:                
                programsSpectrum[idProgram] += [G.number_of_edges()]
        
        elapsedP[idProgram] = time.time() - start
    return elapsedP, programs, graphP, programsSpectrum