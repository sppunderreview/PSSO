import os
import pickle

def readPSSOStudySpeedWithoutPreprocessing():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	ID_RUN = 6
	P = 40
	nQBI = "QB" 
	LC =  ["PSSO_30","PSSO_50","PSSO_80","PSSO_130","PSSO_150","PSSO_180"]
	tableSpeed = {}
	for nEmb in LC:
		RESULTS = []
		for pId in range(P):
			inputFile = os.path.join(ABS_PATH, "../../XP_PSSO_Study/R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN))
			with open(inputFile, "rb") as f:
				RESULTS += pickle.load(f)
		ACC = []
		T = []
		for i in range(1,len(RESULTS), 3):
			ACC += [RESULTS[i]]
			T += [RESULTS[i+1]]
		S = sum(ACC)
		T = sum(T)
		tableSpeed[nEmb] = T
	return tableSpeed
	
#print(readPSSOStudySpeedWithoutPreprocessing())
#{'PSSO_30': 92075.42918586731, 'PSSO_50': 93009.27759385109, 'PSSO_80': 93285.55331611633, 'PSSO_130': 95905.58428382874, 'PSSO_150': 96546.8962392807, 'PSSO_180': 96085.1965432167}
