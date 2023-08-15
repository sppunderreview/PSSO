import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pandas as pd
import pickle

def correctNames(a):
	a = a.replace("PSS_D_5535", "PSS")
	a = a.replace("simCG_D_5535", "simCG")
	a = a.replace("simCFG_D_5535", "simCFG")
	return a

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

from IoT_Preprocessing import readTableIoTPreprocessing

def readIoTAblationSpeed():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksData = {}
	
	LC =  ["PSS_D_5535"]
	ID_RUN = 4
	P = 40
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../XP/R/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ESC = []
		for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
			ESC += [RESULTS[i+2]]
		TSC = sum(ESC)
		
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG"]   = TSC/len(ESC)
		frameworksData[f]["Total"] = TSC

	LC =  ["simCG_D_5535","simCFG_D_5535"]
	ID_RUN = 4
	P = 40
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../XP_Ablation/R/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ESC = []
		for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
			ESC += [RESULTS[i+2]]
		TSC = sum(ESC)
		
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG"]   = TSC/len(ESC)
		frameworksData[f]["Total"] = TSC

		
	tablePreprocessing = readTableIoTPreprocessing()
	tablePreprocessing["simCG"] = tablePreprocessing["PSS"]
	
	
	for f in frameworksData:
		total =    frameworksData[f]["Total"]
		avg    =   frameworksData[f]["AVG"]

		if f in tablePreprocessing:
			total += tablePreprocessing[f]["Total"]
			avg   += tablePreprocessing[f]["Average"]
				
		frameworksData[f]["AVG"] = formatTimeAvg(avg)
		if f in tablePreprocessing:
			frameworksData[f]["AVG"] += " ("+formatTimeAvg(tablePreprocessing[f]["Average"])+ ")"						

		frameworksData[f]["Total"] = formatTime(total)
		if f in tablePreprocessing:
			frameworksData[f]["Total"] += " ("+formatTime(tablePreprocessing[f]["Total"]) + ")"
	
	#df = pd.DataFrame(frameworksData).T
	#df.fillna(0, inplace=True)
	#print(df)
	
	return frameworksData

#readIoTAblationSpeed()
