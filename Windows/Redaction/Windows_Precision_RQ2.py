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

def readWindowsPrecisionRQ2():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksData = {}
	
	# Main experiences
	ID_RUN = 3
	P = 40
	nQBI = "QB"	
	for nEmb in ["LIBDX", "SHAPE","BSIZE","DSIZE", "MUTANTX","PSS","GSA","FUNCTIONSET"]:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH,"../XP/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)					
		ACC = []
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG"] = "{:.3f}".format(sum(ACC)/len(ACC))

	# StringSet experience
	ID_RUN = 3
	P = 80
	nQBI = "QB"
	nEmb = "STRINGS"
	RESULTS = []
	for pId in range(P):
	   for RUN in ["","2","3"]:
		   inputFile = os.path.join(ABS_PATH,"../StringSet/R/R"+RUN+"_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
		   if os.path.isfile(inputFile):
			   with open(inputFile, "rb") as f:
				   RESULTS += pickle.load(f)
	ACC = {}
	for i in range(0,len(RESULTS),3):
	   ACC[RESULTS[i]] = RESULTS[i+1]
	
	ACCL = []
	for idS in ACC:
	   ACCL += [ACC[idS]]
	frameworksData["StringSet"] = {}
	frameworksData["StringSet"]["AVG"] = "{:.3f}".format(sum(ACCL)/len(ACCL))
	
	# PSSO experience
	ID_RUN = 6
	P = 40
	nQBI = "QB" 
	nEmb = "PSSV16"
	RESULTS = []
	for pId in range(P):
		inputFile = os.path.join(ABS_PATH,"../PSSO/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
		with open(inputFile, "rb") as f:
			RESULTS += pickle.load(f)
	ACC = []
	for i in range(1,len(RESULTS), 3):
		ACC += [RESULTS[i]]
	frameworksData["PSSO"] = {}
	frameworksData["PSSO"]["AVG"] = "{:.3f}".format(sum(ACC)/len(ACC))

	#df = pd.DataFrame(frameworksData).T
	#df.fillna(0, inplace=True)		
	#print(df)
	
	return frameworksData

#readWindowsPrecisionRQ2()

