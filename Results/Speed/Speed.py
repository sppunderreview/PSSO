import os
import pickle

import numpy as np

import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd

import random

# Clone search runtimes (without preprocessing)

def formatTime(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = round(s % 60)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"

def formatTimeAvg(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = s % 60
    if h == 0 and m == 0:
        s = round(s,2)
    else:
        s = round(s)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"


frameworks = ["Bsize","Dsize","Shape", "ASCG", "ASCFG","GED-0","MutantX-S","Asm2vec","Gemini","SAFE","PSS","PSSO","GED-L","SMIT","CGC","AlphaDiff","LibDX","LibDB","StringSet","FunctionSet"]
XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]

frameworksData = {}

for framework in frameworks:
    frameworksData[framework] = {}

    globalAvgCS = []
    globalMinCS = 100000
    globalMaxCS = 0
        
    for (nameDS, DS_Couple) in XPS:
        with open("../../"+framework+"/"+nameDS+"_MD", "rb") as f:
            MD3 = pickle.load(f)
            
        y = []
        for nameXP  in DS_Couple:
            outputFile = "../../"+framework+"/"+nameXP+"_MD"

            if os.path.exists(outputFile) == False:
                continue

            with open(outputFile, "rb") as f:
                MD = pickle.load(f)

            for arrow in ["->","<-"]:
                for idS in MD[arrow]:
                    couples = []
                    
                    for idS2 in  MD[arrow][idS]:
                        t = MD[arrow][idS][idS2]

                        
                        if len(t) == 3 or len(t) == 5: 
                            if idS in MD3 and idS2 in MD3[idS]:                    
                                el = MD3[idS][idS2][-1]
                            else:
                                print("ERROR", idS, idS2, nameDS, framework)
                        else:
                            _, _, _ ,_ , d, el = t
                        couples += [el]
                    y += [couples]
        
        for l in y:
            globalAvgCS += [sum(l)]

        minCS = 100000
        maxCS = 0
        for l in y:
            minCS = min(sum(l),minCS)
            maxCS = max(sum(l), maxCS)
                
        globalMinCS = min(globalMinCS, minCS)
        globalMaxCS = max(globalMaxCS, maxCS)    
    globalAvgCS = sum(globalAvgCS)/len(globalAvgCS)

    frameworksData[framework]["Clone Search avg (min,max)"] = formatTimeAvg(globalAvgCS) +  " (" + formatTime(globalMinCS) +"," + formatTime(globalMaxCS) + ")"
    

dfSI = pd.DataFrame(frameworksData).T
dfSI.fillna(0, inplace=True)

print(dfSI)

latex =  dfSI.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

print(latex)


