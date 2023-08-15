import os
import pickle
import pandas as pd

def readWindowsAblationPrecision():
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
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
		f = nEmb
		frameworksData[f] = {}
		frameworksData[f]["AVG"] = "{:.3f}".format(sum(ACC)/len(ACC))

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
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
		f = nEmb
		frameworksData[f] = {}
		frameworksData[f]["AVG"] = "{:.3f}".format(sum(ACC)/len(ACC))



	#df = pd.DataFrame(frameworksData).T
	#df.fillna(0, inplace=True)		
	#print(df)
	
	return frameworksData

#readWindowsAblationPrecision()

