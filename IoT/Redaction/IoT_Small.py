import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pandas as pd
import pickle

def correctNames(a):
	a = a.replace("STRINGS", "StringSet")
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

def readIoTSmall():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksData = {}
	
	LC =  ["STRINGS"]
	ID_RUN = 4
	P = 1
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../XP/RS/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ESC = []
		ACC = []		
		for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
			ESC += [RESULTS[i+2]]
			ACC += [RESULTS[i+1]]
		S = sum(ACC)
		TSC = sum(ESC)
		
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG Clone Search (s)"]   = formatTimeAvg(TSC/len(ESC))
		frameworksData[f]["Total Clone Search (s)"] = formatTime(TSC)
		frameworksData[f]["Precision"] = "{:.3f}".format(S/len(ACC))
	
	df = pd.DataFrame(frameworksData).T
	df.fillna(0, inplace=True)
	print(df)
	
	return frameworksData

readIoTSmall()
