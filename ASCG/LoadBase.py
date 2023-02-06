import json
import time

def loadGraphs(inputs):
    elapsedP = {}
    functionName = {}
    programs = {}
    graphP = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:
        start = time.time()

        with open(pathJson) as f:
          data = json.load(f)
          
        idProgram = str(idS)
        programs[idProgram] = True
        graphP[idProgram] = {}
        
        for f in data["functions"]:
            idFunction = "P_"+idProgram+"F_"+str(f["id"])
            functionName[idFunction] = f["name"]
            
            graphP[idProgram][idFunction] = []
            
            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphP[idProgram][idFunction] += [idNF]
            
            
        elapsedP[idProgram] = time.time() - start

    return elapsedP, programs, graphP,  functionName
