import os
import pickle

def readPSSOStudyPreprocessing():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	with open(os.path.join(ABS_PATH,"QB"), "rb") as f:
		E = pickle.load(f) # [Q,B,I,QNames]
		Q = E[0]
		B = E[1]
		I = E[2]
		QNames = E[3]

	tablePrepro = {}

	for nEmb in ["PSSO_30","PSSO_50","PSSO_80","PSSO_130","PSSO_150","PSSO_180"]:
		with open(os.path.join(ABS_PATH, "Prepro_"+nEmb), "rb") as f:
			T = pickle.load(f)
		P = []
		for idS in Q:
			if idS in T:
				P += [T[idS]]
		PMeans = sum(P)/len(P)    
		tablePrepro[nEmb] = PMeans

	return tablePrepro
