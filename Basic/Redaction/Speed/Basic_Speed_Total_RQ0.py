import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pickle
import numpy as np
import pandas as pd

def formatTime(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = round(s % 60)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"

def formatTimeAvg(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = s % 60
    if h == 0 and m == 0:
        s = round(s,2)
    else:
        s = round(s)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"

from Basic_Preprocessing import readTableBasicPreprocessing

def readBasicSpeedTotalRQ0():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])

	frameworks = ["Bsize","Dsize","Shape", "ASCG", "ASCFG","GED-0","MutantX-S","Asm2vec","Gemini","SAFE","PSS","PSSO","GED-L","SMIT","CGC","AlphaDiff","LibDX","LibDB","StringSet","FunctionSet"]
	XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]

	frameworksData = {}

	for framework in frameworks:
		frameworksData[framework] = {}
		elapsed = {}    
			
		for (nameDS, DS_Couple) in XPS:
			with open(os.path.join(ABS_PATH, "../../../"+framework+"/"+nameDS+"_MD"), "rb") as f:
				MD3 = pickle.load(f)
				
			y = []
			for nameXP  in DS_Couple:
				outputFile = os.path.join(ABS_PATH, "../../../"+framework+"/"+nameXP+"_MD")

				if os.path.exists(outputFile) == False:
					continue

				with open(outputFile, "rb") as f:
					MD = pickle.load(f)

				for arrow in ["->","<-"]:
					for idS in MD[arrow]:
						couples = []
						
						for idS2 in  MD[arrow][idS]:
							t = MD[arrow][idS][idS2]

							
							if framework in ["LibDB"]:
								el = t[-1]
								d  = t[-2]
								if d == 1: 
									el = 0
							elif len(t) == 3 or len(t) == 5: 
								if idS in MD3 and idS2 in MD3[idS]:                    
									el = MD3[idS][idS2][-1]
							else:
								el = t[-1]
							
							identifier = nameDS+"_"+str(idS)+"_"+str(idS2)
							if identifier in elapsed:
								continue
							elapsed[identifier] = el
		
		
		globalTotal = 0
		for identifier in elapsed:
			globalTotal += elapsed[identifier]
		frameworksData[framework]["Total"] = globalTotal

	tablePreprocessing = readTableBasicPreprocessing()


	for f in frameworksData:
		elapsedTotal = frameworksData[f]["Total"]
		if f in tablePreprocessing:
			elapsedTotal += tablePreprocessing[f]["Total"] 
		frameworksData[f]["Total"] = formatTime(elapsedTotal)


	dfSISpeed = pd.DataFrame(frameworksData).T
	dfSISpeed.fillna(0, inplace=True)

	print("Table (RQ0) Total runtimes on the Basic dataset")
	print(dfSISpeed)


