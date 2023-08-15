import os
import pickle
import pandas as pd

def readTableBinkitAblationPreprocessing():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    	
	with open(os.path.join(ABS_PATH,"../ELAPSED_SCs_NORMAL"), "rb") as f:
		ELAPSED_SCs_NORMAL  = pickle.load(f)

	with open(os.path.join(ABS_PATH, "../ELAPSED_SCs_OBF"), "rb") as f:
		ELAPSED_SCs_OBF = pickle.load(f)

	#print([x for x in ELAPSED_SCs_NORMAL])
	#print([x for x in ELAPSED_SCs_OBF])

	ELAPSED_SCs = ELAPSED_SCs_NORMAL

	for nEmb in ELAPSED_SCs_OBF:    
		for idS in ELAPSED_SCs_OBF[nEmb]:
			if not(idS in ELAPSED_SCs[nEmb]):
				ELAPSED_SCs[nEmb][idS] = ELAPSED_SCs_OBF[nEmb][idS]
			else:
				ELAPSED_SCs[nEmb][idS] += ELAPSED_SCs_OBF[nEmb][idS]

	with open(os.path.join(ABS_PATH, "../Preproccesing_EMBEDS"), "rb") as f:
		QP_EMBS = pickle.load(f)

	frameworksPlot = {}
			
	for nEmb in ["PSS"]:
		QPs = 0
		N = 0
		for idS in ELAPSED_SCs[nEmb]:
			QPs += QP_EMBS[nEmb][idS] * len(ELAPSED_SCs[nEmb][idS])
			N += len(ELAPSED_SCs[nEmb][idS])
		
		framework = nEmb.replace("PSSV16","PSSO")
		framework = framework.replace("SCG","ASCG")
		frameworksPlot[framework] = {}
		frameworksPlot[framework]["Total"] = QPs
		frameworksPlot[framework]["Average"] = QPs/N

	frameworksPlot["simCG"] = frameworksPlot["PSS"]
	#df = pd.DataFrame(frameworksPlot).T
	#df.fillna(0, inplace=True)
	#print(df)
	return frameworksPlot

#readTableBinkitAblationPreprocessing()
