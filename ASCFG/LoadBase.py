import json

def loadGraphs(inputs):
    functionName = {}
    programs = {}
    graphP = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:
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
            
            

    return programs, graphP,  functionName
