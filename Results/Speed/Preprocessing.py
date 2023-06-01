import os
import pickle

import numpy as np

import pandas as pd

import random

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

frameworks = ["ASCG", "ASCFG","PSS","PSSO"]
XPS = ["CV","CO","UV","UO","BV","BO"]

frameworksPlot = {}

for framework in frameworks:
    frameworksPlot[framework] = {}    
    for nameDS in XPS:
        y = []
        
        outputFile = "../../"+framework+"/A_"+nameDS
        if os.path.exists(outputFile) == False:
            continue

        with open(outputFile, "rb") as f:
            D = pickle.load(f)

        if os.path.exists(outputFile+"_C"):
            with open(outputFile+"_C", "rb") as f:
                DC = pickle.load(f)
                for x in DC:
                    D[x] = DC[x]
            
        for idS in D:
            y += [D[idS][-1]]
        frameworksPlot[framework][nameDS] = y
        

table = {}
for framework in frameworksPlot:
    table[framework] = {}
    AVG = []
    totalY = []
    for nameDS in frameworksPlot[framework]:
        # Correction
        # Each Basic dataset has six different test fields (e.g., O0O1, O0O2, O0O3, O1O2, O1O3, O2O3).
        # Since a program is inside 3 test fields, we perform three clone searches for each program.
        # Therefore, we have to measure three times the preprocessing of each program.
        # The total preprocessing running times of ASCG, ASCFG, PSS, and PSSO must be multiplied by 3."""
        totalY += frameworksPlot[framework][nameDS]
        totalY += frameworksPlot[framework][nameDS]
        totalY += frameworksPlot[framework][nameDS]
        AVG += frameworksPlot[framework][nameDS]
    
    print(len(totalY))
    minF = min(totalY)
    maxF = max(totalY)
    totalF = sum(totalY)
    avgF = sum(AVG)/len(AVG)
    
    table[framework]["Total"] = formatTime(totalF)
    table[framework]["Maximum"] = formatTime(maxF)
    table[framework]["Average"] = formatTimeAvg(avgF)
    

df = pd.DataFrame(table).T
df.fillna(0, inplace=True)

print(df)

latex =  df.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

print(latex)

