import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pickle
import pandas as pd

def correctNames(a):
	a = a.replace("PSSV16", "PSSO")
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

from Windows_Preprocessing import readTableWindowsPreprocessing


def readWindowsSmall():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksData = {}
	
	# PSSO experience
	ID_RUN = 6
	P = 1
	nQBI = "QB" 
	nEmb = "PSSV16"
	RESULTS = []
	for pId in range(P):
		inputFile = os.path.join(ABS_PATH,"../PSSO/RS/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
		with open(inputFile, "rb") as f:
			RESULTS += pickle.load(f)
	ACC = []
	T = []
	for i in range(1,len(RESULTS), 3):
		ACC += [RESULTS[i]]
		T += [RESULTS[i+1]]
	frameworksData["PSSO"] = {}
	frameworksData["PSSO"]["Total Clone Search (s)"] = sum(T)
	frameworksData["PSSO"]["AVG Clone Search (s)"] = sum(T)/len(T)	
	frameworksData["PSSO"]["Precision"] = "{:.3f}".format(sum(ACC)/len(ACC))

	# Add preprocessing informations	
	tablePreprocessing = readTableWindowsPreprocessing()	
	for f in frameworksData:
		total = frameworksData[f]["Total Clone Search (s)"]
		avg   = frameworksData[f]["AVG Clone Search (s)"]
		if f in tablePreprocessing:
			total += tablePreprocessing[f]["Total"]
			avg   += tablePreprocessing[f]["Average"]
				
		frameworksData[f]["AVG Clone Search (s)"] = formatTimeAvg(avg)
		if f in tablePreprocessing:
			frameworksData[f]["AVG Clone Search (s)"] += " ("+formatTimeAvg(tablePreprocessing[f]["Average"])+ ")"						

		frameworksData[f]["Total Clone Search (s)"] = formatTime(total)
		if f in tablePreprocessing:
			frameworksData[f]["Total Clone Search (s)"] += " ("+formatTime(tablePreprocessing[f]["Total"]) + ")"

	df = pd.DataFrame(frameworksData).T
	df.fillna(0, inplace=True)		
	print(df)
	
	return frameworksData

readWindowsSmall()

