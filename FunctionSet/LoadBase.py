import json
 
def loadGraphs(inputs):
    programs = {}
    programsExtern = {}
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        with open(pathJson) as f:
          data = json.load(f)
        
        idProgram = str(idS)
        programs[idProgram] = True
        programsExtern[idProgram] = set()

        for f in data["functions"]:
            instruction = ""
            for b in f["blocks"]:
                for instr in b["src"]:
                    instruction = instr[1]
                    break
                if instruction != "":
                    break
            # We get the name of extern functions
            if instruction == "extrn" or instruction == "":
                programsExtern[idProgram].add(f["name"])
                    
    return programs, programsExtern
 
