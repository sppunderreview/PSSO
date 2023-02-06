import json

def loadGraphs(inputs):
    programsNE = {}

    graphPSuccs = {}
    graphPPreds = {}
    
    functionsData = {}
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        with open(pathJson) as f:
          data = json.load(f)
          
        idProgram = str(idS)
        programsNE[idProgram] = 0
        
        graphPSuccs[idProgram] = {}
        graphPPreds[idProgram] = {}
        
        functionsData[idProgram] = {}
        
        
        for f in data["functions"]:
            idFunction = "P_"+idProgram+"F_"+str(f["id"])
            functionsData[idProgram][idFunction] = {}
            
            graphPSuccs[idProgram][idFunction] = []

            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphPSuccs[idProgram][idFunction] += [idNF]
                if not(idNF in graphPPreds[idProgram]):
                    graphPPreds[idProgram][idNF] = []
                graphPPreds[idProgram][idNF] += [idFunction]
                programsNE[idProgram] += 1
    
    for p in functionsData:
        for f in functionsData[p]:
            
            if not(f in graphPSuccs[p]):
                graphPSuccs[p][f] = []
            if not(f in graphPPreds[p]):
                graphPPreds[p][f] = []
                
    return functionsData, graphPPreds, graphPSuccs, programsNE
