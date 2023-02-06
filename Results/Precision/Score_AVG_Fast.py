import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random

frameworks = ["Bsize","Dsize","Shape", "ASCG", "MutantX-S","PSS","PSSO","LibDX","StringSet","FunctionSet"]


XPS  =  [("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]
XPS  += [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"])]

frameworkPlot = {}

for framework in frameworks:    
    for (nameDS, DS_Couple) in XPS:
        for nameXP  in DS_Couple:
            y = []
            outputFile = "../../"+framework+"/"+nameXP+"_MD"

            if os.path.exists(outputFile) == False:
                continue

            with open(outputFile, "rb") as f:
                MD = pickle.load(f)
            
            for idS in MD["->"]:
                couples = []
                
                for idS2 in  MD["->"][idS]:                    
                    t = MD["->"][idS][idS2]

                    if len(t) == 3:
                        name,name2,d = t 
                    elif len(t) == 5:
                        name, name2, _ ,_ , d = t
                    else:
                        name, name2, _ ,_ , d, _ = t
                        
                    # correct a wrong file name
                    if name == "acyclic":
                        name = "dot"
                    if name2 == "acyclic":
                        name2 = "dot"
                            
                    if name == name2:
                        couples += [(True,d)]
                    else:
                        couples += [(False,d)]
                random.shuffle(couples)
                y += [couples]
                
            for idS in MD["<-"]:
                couples = []
                
                for idS2 in  MD["<-"][idS]:
                    t = MD["<-"][idS][idS2]
                        
                    if len(t) == 3:
                        name,name2,d = t 
                    elif len(t) == 5:
                        name, name2, _ ,_ , d = t
                    else:
                        name, name2, _ ,_ , d, _ = t

                    # correct a wrong file name
                    if name == "acyclic":
                        name = "dot"
                    if name2 == "acyclic":
                        name2 = "dot"

                    if name == name2:
                        couples += [(True,d)]
                    else:
                        couples += [(False,d)]
                random.shuffle(couples)                        
                y += [couples]
            if len(y) == 0:
                continue
            
            ACC = []        
            for L in y :        
                L.sort(key=lambda x: x[1])
                candidates = []            
                for (t,d) in L:
                    if d == L[0][1]:
                        candidates += [t]
                    else:
                        break
                ACC += [random.choice(candidates)]
            
            nameField = nameXP[1:]
            if not(framework in frameworkPlot):
                frameworkPlot[framework] = {}
                
            if not(nameField in frameworkPlot[framework]):
                frameworkPlot[framework][nameField] = []
            frameworkPlot[framework][nameField] += ACC
            

    
dataTable = {}
for framework in frameworkPlot:
    dataTable[framework] = {}
    T = []
    for nameField in frameworkPlot[framework]:
        T += [sum(frameworkPlot[framework][nameField])/len(frameworkPlot[framework][nameField])]        
    dataTable[framework]["AVG"] = "{:.2f}".format(sum(T)/len(T))

dfScenario = pd.DataFrame(dataTable).T
dfScenario.fillna(0, inplace=True)

print(dfScenario)

latex =  dfScenario.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")


print(latex)


