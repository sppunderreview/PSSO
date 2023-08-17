import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
from copy import deepcopy


def readPSSOStudyPrecision():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	ID_RUN = 6
	P = 40
	nQBI = "QB" 
	LC =  ["PSSO_30","PSSO_50","PSSO_80","PSSO_130","PSSO_150","PSSO_180"]
	tablePrecision = {}
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
		tablePrecision[nEmb] = S/len(ACC)
	return tablePrecision
	
print(readPSSOStudyPrecision())
