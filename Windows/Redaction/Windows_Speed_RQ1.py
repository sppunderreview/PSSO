import os
import pickle
import pandas as pd

def correctNames(a):
	a = a.replace("PSSV16", "PSSO")
	a = a.replace("GSA", "ASCG")
	a = a.replace("MUTANTX", "MutantX-S")
	a = a.replace("DSIZE", "Dsize")
	a = a.replace("BSIZE", "Bsize")
	a = a.replace("FUNCTIONSET", "FunctionSet")
	a = a.replace("SHAPE", "Shape")
	a = a.replace("STRINGS", "StringSet")
	a = a.replace("LIBDX", "LibDX")
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


def readWindowsSpeedRQ1():	
	frameworksData = {}
	
	# Main experiences
	ID_RUN = 3
	P = 40
	nQBI = "QB"	
	for nEmb in ["LIBDX", "SHAPE","BSIZE","DSIZE", "MUTANTX","PSS","GSA","FUNCTIONSET"]:
		RESULTS = []
		for pId in range(P):
			inputFile = "../XP/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)					
		ACC = []
		T = []				
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
			T += [RESULTS[i+1]]		
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["Total"] = sum(T)
		frameworksData[f]["AVG"] = sum(T)/len(T)

	# StringSet experience
	ID_RUN = 3
	P = 80
	nQBI = "QB"
	nEmb = "STRINGS"
	RESULTS = []
	for pId in range(P):
	   for RUN in ["","2","3"]:
		   inputFile = "../StringSet/R/R"+RUN+"_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
		   if os.path.isfile(inputFile):
			   with open(inputFile, "rb") as f:
				   RESULTS += pickle.load(f)
	ACC = {}
	T = {}
	for i in range(0,len(RESULTS),3):
	   ACC[RESULTS[i]] = RESULTS[i+1]
	   T[RESULTS[i]] =  RESULTS[i+2]
	
	ACCL = []
	TL = []
	for idS in ACC:
	   ACCL += [ACC[idS]]
	   TL += [T[idS]]
	frameworksData["StringSet"] = {}
	frameworksData["StringSet"]["Total"] = sum(TL)
	frameworksData["StringSet"]["AVG"] = sum(TL)/len(TL)
	
	# PSSO experience
	ID_RUN = 6
	P = 40
	nQBI = "QB" 
	nEmb = "PSSV16"
	RESULTS = []
	for pId in range(P):
		inputFile = "../PSSO/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
		with open(inputFile, "rb") as f:
			RESULTS += pickle.load(f)
	ACC = []
	T = []
	for i in range(1,len(RESULTS), 3):
		ACC += [RESULTS[i]]
		T += [RESULTS[i+1]]
	frameworksData["PSSO"] = {}
	frameworksData["PSSO"]["Total"] = sum(T)
	frameworksData["PSSO"]["AVG"] = sum(T)/len(T)	

	# Add preprocessing informations	
	tablePreprocessing = readTableWindowsPreprocessing()	
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

#readWindowsSpeedRQ1()

