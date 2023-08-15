import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pickle
import pandas as pd

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

from Binkit_Ablation_Preprocessing import readTableBinkitAblationPreprocessing

def readBinkitAblationSpeed():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    
	with open(os.path.join(ABS_PATH,"ELAPSED_SCs_Ablation_NORMAL"), "rb") as f:
		ELAPSED_SCs_NORMAL  = pickle.load(f)

	with open(os.path.join(ABS_PATH, "ELAPSED_SCs_Ablation_OBF"), "rb") as f:
		ELAPSED_SCs_OBF = pickle.load(f)

	ELAPSED_SCs = ELAPSED_SCs_NORMAL

	for nEmb in ELAPSED_SCs_OBF:    
		for idS in ELAPSED_SCs_OBF[nEmb]:
			if not(idS in ELAPSED_SCs[nEmb]):
				ELAPSED_SCs[nEmb][idS] = ELAPSED_SCs_OBF[nEmb][idS]
			else:
				ELAPSED_SCs[nEmb][idS] += ELAPSED_SCs_OBF[nEmb][idS]
	
	tablePreprocessing = readTableBinkitAblationPreprocessing()
	frameworksData = {}
	
	for nEmb in ELAPSED_SCs:
		SCs = 0
		N = 0
		for idS in ELAPSED_SCs[nEmb]:
			SCs += sum(ELAPSED_SCs[nEmb][idS])
			N += len(ELAPSED_SCs[nEmb][idS])				
		
		total  = SCs
		avg    = SCs/N
		
		f = nEmb
		frameworksData[f] = {}
	
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

#readBinkitAblationSpeed()
