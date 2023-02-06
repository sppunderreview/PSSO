import json
import networkx as nx 



def makeDot(lAdj, functionName):
    txt = "graph G{\n"
    txt += "node[label=\"\"];\n"
    
    for x in lAdj:
        for y in lAdj[x]:
            nameX = functionName[x]
            nameY = functionName[y]
            if "sub_" in nameX and "sub_" in nameY:
                txt += "\""+nameX+"\" -- \""+nameY+"\";\n"
     
    return txt+"}\n"
    
def makeGraph(lAdj, functionName):
    #print(len(lAdj))
    G = nx.Graph()
    for x in lAdj:
        for y in lAdj[x]:
            nameX = functionName[x]
            if not(y in functionName):
                continue
            nameY = functionName[y]
            if nameX == nameY:
                continue
            #if "sub_" in nameX and "sub_" in nameY:
            G.add_edge(nameX, nameY)
    return G
    
def loadGraphs(inputs):
    functionName = {}
    graphP = {}
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        with open(pathJson) as f:
          data = json.load(f)
          
        idProgram = str(idS)
        graphP[idProgram] = {}
        
        for f in data["functions"]:
            idFunction = "P_"+idProgram+"F_"+str(f["id"])
            functionName[idFunction] = f["name"]
            
            
            graphP[idProgram][idFunction] = []
            
            for nextF in f["call"]:
                idNF = "P_"+idProgram+"F_"+str(nextF)
                graphP[idProgram][idFunction] += [idNF]
            


    
    for idS in graphP:
        graphP[idS] = makeGraph(graphP[idS] , functionName)
    
    return graphP
