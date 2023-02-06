import json

def loadGraphs(inputs):
    programsNE = {}

    graphPSuccs = {}
    graphPPreds = {}
    
    functionsData = {}
    
    totalF = 0
    totalExtern = 0

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
            
            functionsData[idProgram][idFunction]["name"] = f["name"]
            
            
            
            graphPSuccs[idProgram][idFunction] = []

            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphPSuccs[idProgram][idFunction] += [idNF]
                if not(idNF in graphPPreds[idProgram]):
                    graphPPreds[idProgram][idNF] = []
                graphPPreds[idProgram][idNF] += [idFunction]
                
                programsNE[idProgram] += 1
            
            instructions = []
            for b in f["blocks"]:
                for instr in b["src"]:
                    instructions += [instr[1]]


            #functionsData[idProgram][idFunction]["instructions"] = instructions
            functionsData[idProgram][idFunction]["mnemonics"] = (instructions, str(instructions))
            functionsData[idProgram][idFunction]["len"] = len(instructions)
            functionsData[idProgram][idFunction]["extern"] = len(instructions) == 0 or (instructions[0] == "extrn")
            
            if not(functionsData[idProgram][idFunction]["extern"]):
                totalF += 1
            else:
                totalExtern += 1
    
    for p in functionsData:
        for f in functionsData[p]:
            #functionsData[p][f]["degree"] = 0
            
            if not(f in graphPSuccs[p]):
                graphPSuccs[p][f] = []
            if not(f in graphPPreds[p]):
                graphPPreds[p][f] = []
                
        
    """for p in graphPSuccs:
        for f in graphPSuccs[p]:
            functionsData[p][f]["degree"] += len(graphPSuccs[p][f])

    for p in graphPPreds:
        for f in graphPPreds[p]:
            if f in functionsData[p]:
                functionsData[p][f]["degree"] += len(graphPPreds[p][f])"""
    
    """for p in graphPSuccs:
        for f in graphPSuccs[p]:
            succExternal = []
            for s in graphPSuccs[p][f]:
                if s in functionsData[p] and functionsData[p][s]["extern"]:
                    succExternal += [functionsData[p][s]["name"]]
            functionsData[p][f]["externalCalls"] = succExternal"""
    
    #print("Total F", totalF)
    #print("EXTERN", totalExtern)
    return functionsData, graphPPreds, graphPSuccs, programsNE
