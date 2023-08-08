import os
import pickle
import pandas as pd

def readTableWindowsPreprocessing():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	frameworksPlot = {}

	nQBI = "QB"
	with open(os.path.join(ABS_PATH,nQBI), "rb") as f:
		E = pickle.load(f) # [Q,B,I,QNames]
		Q = E[0]

	with open(os.path.join(ABS_PATH,"preprocessQPSS"), "rb") as f:
		preprocessQPSS = pickle.load(f)

	with open(os.path.join(ABS_PATH,"preprocessQASCG"), "rb") as f:
		preprocessQASCG = pickle.load(f)

	with open(os.path.join(ABS_PATH,"preprocessQPSSO"), "rb") as f:
		preprocessQPSSO = pickle.load(f)

		
	with open(os.path.join(ABS_PATH,"SPECTRUM_PREPROCESSING_PSS_CORRECTED"), "rb") as f:
		SPECTRUM_PSSC = pickle.load(f)

	# Correct runnting times for large graphs (see the README):
	for idS in preprocessQPSS:
		if preprocessQPSS[idS][1] > 50000:
			preprocessQPSS[idS] =  [SPECTRUM_PSSC[idS][1],None]
	for idS in preprocessQASCG:
		if preprocessQASCG[idS][1] > 50000:
			preprocessQASCG[idS] = [SPECTRUM_PSSC[idS][1],None]

	for nEmb in ["PSS","ASCG","PSSO"]:
		P = []
		if nEmb == "PSS":
			P = [preprocessQPSS[idS][0] for idS in Q if idS in preprocessQPSS]
		elif nEmb == "ASCG":
			P = [preprocessQASCG[idS][0] for idS in Q if idS in preprocessQASCG]
		elif nEmb == "PSSO":
			P = [preprocessQPSSO[idS] for idS in Q if idS in preprocessQPSSO]
		
		total = sum(P)
		avg   = sum(P)/len(P)

		frameworksPlot[nEmb] = {}
		frameworksPlot[nEmb]["Total"] = sum(P)
		frameworksPlot[nEmb]["Average"] = sum(P)/len(P)
	#df = pd.DataFrame(frameworksPlot).T
	#df.fillna(0, inplace=True)
	#print(df)
	
	return frameworksPlot

#readTableWindowsPreprocessing()
