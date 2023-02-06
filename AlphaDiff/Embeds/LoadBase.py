
import json
import networkx as nx 


def loadGraphs(inputs):
    programs = {}
    
    ExernsP = {}
    graphP = {}
    graphFName = {}
    functionsData = {}
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        with open(pathJson) as f:
          data = json.load(f)
        
        idProgram = str(idS)
        programs[idProgram] = True
        ExernsP[idProgram] = set()
        graphP[idProgram] = {}
        graphFName[idProgram] = {}
        functionsData[idProgram] = {}
        
        
        for f in data["functions"]:
            idFunction = "P_"+idProgram+"F_"+str(f["id"])            
            graphP[idProgram][idFunction] = []
            graphFName[idProgram][idFunction] = f["name"]
            
            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphP[idProgram][idFunction] += [idNF]

            instruction = ""
            for b in f["blocks"]:
                for instr in b["src"]:
                    instruction = instr[1]
                    break
                if instruction != "":
                    break
            # We get the name of extern functions
            if instruction == "extrn" or instruction == "":
                ExernsP[idProgram].add(f["name"])
            
            asm = ""
            for b in f["blocks"]:
                if "bytes" in b:
                    asm += b["bytes"]
                    
            functionsData[idProgram][idFunction] =  asm
            
    return programs, ExernsP, graphP, graphFName, functionsData
    

