import os
import pickle
import pandas as pd


def readTableIoTPreprocessing():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    
	frameworksPlot = {}
			
	for framework in ["PSS", "ASCG","PSSO"]:		
		with open(os.path.join(ABS_PATH, "preprocessQ"+framework), "rb") as f:
			preprocessQ = pickle.load(f)
			preprocessQ = [preprocessQ[idS] for idS in preprocessQ]
			
		frameworksPlot[framework] = {}
		frameworksPlot[framework]["Total"] = sum(preprocessQ)
		frameworksPlot[framework]["Average"] = sum(preprocessQ)/len(preprocessQ)
	#df = pd.DataFrame(frameworksPlot).T
	#df.fillna(0, inplace=True)
	#print(df)
	return frameworksPlot

#readTableIoTPreprocessing()
