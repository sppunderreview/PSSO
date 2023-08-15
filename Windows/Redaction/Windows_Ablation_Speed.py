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

from Windows_Preprocessing import readTableWindowsPreprocessing


def readWindowsAblationSpeed():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksData = {}
	
	# Main experiences
	ID_RUN = 3
	P = 40
	nQBI = "QB"	
	for nEmb in ["PSS"]:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH,"../XP/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)					
		ACC = []
		T = []				
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
			T += [RESULTS[i+1]]		
		f = nEmb
		frameworksData[f] = {}
		frameworksData[f]["Total"] = sum(T)
		frameworksData[f]["AVG"] = sum(T)/len(T)

	# Ablation
	ID_RUN = 3
	P = 40
	nQBI = "QB"	
	for nEmb in ["simCG","simCFG"]:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH,"../XP_Ablation/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)					
		ACC = []
		T = []				
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
			T += [RESULTS[i+1]]		
		f = nEmb
		frameworksData[f] = {}
		frameworksData[f]["Total"] = sum(T)
		frameworksData[f]["AVG"] = sum(T)/len(T)


	# Add preprocessing informations	
	tablePreprocessing = readTableWindowsPreprocessing()
	tablePreprocessing["simCG"] = tablePreprocessing["PSS"]
	
	for f in frameworksData:
		total = frameworksData[f]["Total"]
		avg   = frameworksData[f]["AVG"]
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

#readWindowsAblationSpeed()

