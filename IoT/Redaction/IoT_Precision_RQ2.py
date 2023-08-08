import os
import pandas as pd
import pickle

def correctNames(a):
	a = a.replace("PSS_D_5535", "PSS")
	a = a.replace("PSSV16", "PSSO")
	a = a.replace("SCG_D_5535", "ASCG")
	a = a.replace("MUTANTX2", "MutantX-S")
	a = a.replace("MUTANTX", "REMOVED")
	a = a.replace("DSIZE", "Dsize")
	a = a.replace("BSIZE", "Bsize")
	a = a.replace("FUNCTIONSET", "FunctionSet")
	a = a.replace("SHAPE", "Shape")
	a = a.replace("STRINGS", "StringSet")
	a = a.replace("LIBDX", "LibDX")
	return a
	

def readIoTPrecicionRQ2():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    
	frameworksData = {}
	
	LC =  ["STRINGS","LIBDX","SHAPE","BSIZE","DSIZE","PSS_D_5535","SCG_D_5535","FUNCTIONSET"]
	ID_RUN = 4
	P = 40
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../XP/R/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ACC = []
		#ESC = []
		for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
			ACC += [RESULTS[i+1]]
			#ESC += [RESULTS[i+2]]
		S = sum(ACC)
		#TSC = sum(ESC)
		
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG"] = "{:.3f}".format(S/len(ACC))
		#print(nEmb, S, len(ACC), S/len(ACC), TSC, TSC/len(ESC))
		

	LC =  ["PSSV16","MUTANTX2"]
	ID_RUN = 4
	P = 40
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../MutantXSV2_PSSO/R/R_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ACC = []
		#ESC = []
		for i in range(0, len(RESULTS),3): # += [idS, S, elapsed]
			ACC += [RESULTS[i+1]]
			#ESC += [RESULTS[i+2]]
		S = sum(ACC)
		#TSC = sum(ESC)
		f = correctNames(nEmb)
		frameworksData[f] = {}
		frameworksData[f]["AVG"] = "{:.3f}".format(S/len(ACC)) 
		#print(nEmb, S, len(ACC), S/len(ACC), TSC, TSC/len(ESC))

	
	#df = pd.DataFrame(frameworksData).T
	#df.fillna(0, inplace=True)
	#print(df)
	
	return frameworksData

#readIoTPrecicionRQ2()
