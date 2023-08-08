import os
import pickle

import numpy as np

#from sklearn import metrics
from scipy import stats
import pandas as pd

import random

def readBasicRobustness_RQ3():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])


	frameworks = ["Bsize","Dsize","Shape", "ASCG", "ASCFG","GED-0","MutantX-S","Asm2vec","Gemini","SAFE","PSS","PSSO","GED-L","SMIT","CGC","AlphaDiff","LibDX","LibDB_Robustness","StringSet","FunctionSet"]

	XPS = [("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]


	dataPoints = {}

	# Collect optimization information among datasets
	dictidSTooptim = {}

	for framework in ["PSS"]:    
		for (nameDS, DS_Couple) in XPS:
			#print(nameDS,framework)
			dictidSTooptim[nameDS] = {}
			
			for nameXP  in DS_Couple:
				outputFile = os.path.join(ABS_PATH, "../../../"+framework+"/"+nameXP+"_MD")        
				if os.path.exists(outputFile) == False:
					continue
				with open(outputFile, "rb") as f:
					MD = pickle.load(f)

				for idS in MD["<>"]:
					couples = []
					for idS2 in  MD["<>"][idS]:
						t = MD["<>"][idS][idS2]
						optim = t[2]
						dictidSTooptim[nameDS][idS] = optim
						break
						
			
	# Computes correlations
	for framework in frameworks:    
		dataPoints[framework] = {}

		for (nameDS, DS_Couple) in XPS:
			y = []
			
			for nameXP  in DS_Couple:
				outputFile = os.path.join(ABS_PATH, "../../../"+framework+"/"+nameXP+"_MD")
				if os.path.exists(outputFile) == False:
					continue

				with open(outputFile, "rb") as f:
					MD = pickle.load(f)

				for idS in MD["<>"]:
					couples = []
					
					for idS2 in  MD["<>"][idS]:
						t = MD["<>"][idS][idS2]
						if len(t) == 3:
							_,_,d = t 
						elif len(t) == 5:
							_, _,_,_,d = t
						else:
							_, _, _ ,_ , d, _ = t                        
						optim  = dictidSTooptim[nameDS][idS]
						optim2 = dictidSTooptim[nameDS][idS2]
						couples += [(optim==optim2,d)]
					random.shuffle(couples)                                                                
					y += [couples]

			if len(y) == 0:
				continue
			



			# Rank-biserial correlation
			
			rankBiserialCorr = []
			for L in y :
				L.sort(key=lambda x: x[1])
				A = []
				B = []


				for i in range(len(L)):
					if L[i][0]:
						A += [i]
					else:
						B += [i]
				

				total = len(A)*len(B)
				supportH = 0
				dontSupportH = 0
				for x in A:
					for y in B:
						if   x < y:
							supportH += 1
						elif y < x:
							dontSupportH += 1

				rankBiserialCorr += [(supportH-dontSupportH)/total]
				
			rankBiserialCorr = np.array(rankBiserialCorr)
			meanBC = stats.describe(rankBiserialCorr).mean
			#print(framework, nameDS, finalDistrRankBiserialCorr.skewness,finalDistrRankBiserialCorr.kurtosis)
			#stdE = stats.tstd(rankBiserialCorr)
			dataPoints[framework][nameDS] = meanBC 

		L = [dataPoints[framework][nameDS] for nameDS in dataPoints[framework]]
		dataPoints[framework]["Average"] = sum(L)/len(L)

		for nameDS in dataPoints[framework]:
			if  dataPoints[framework][nameDS] < 0.16:
				T = "\\textbf{"+"{0:.2f}".format(dataPoints[framework][nameDS]) + "}"
			else:
				T = "{"+"{0:.2f}".format(dataPoints[framework][nameDS]) + "}"        
			dataPoints[framework][nameDS] = T

	print("Table (RQ3) Average rank-biserial correlation for H on the Basic dataset.")
	df = pd.DataFrame(dataPoints).transpose()
	print(df)
