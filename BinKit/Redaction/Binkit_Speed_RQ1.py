import pickle
import pandas as pd

def correctNames(a):
	a = a.replace("PSSV16", "PSSO")
	a = a.replace("SCG ", "ASCG")
	a = a.replace("MUTANTX2", "MutantX-S")
	a = a.replace("MUTANTX", "REMOVED")
	a = a.replace("DSIZE", "Dsize")
	a = a.replace("BSIZE", "Bsize")
	a = a.replace("FUNCTIONSET", "FunctionSet")
	a = a.replace("SHAPE", "Shape")
	a = a.replace("STRINGS", "StringSet")
	a = a.replace("LibDX", "LibDX")
	return a

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

from Binkit_Preprocessing import readTableBinkitPreprocessing

def readBinkitSpeedRQ1():    
	with open("ELAPSED_SCs_NORMAL", "rb") as f:
		ELAPSED_SCs_NORMAL  = pickle.load(f)

	with open("ELAPSED_SCs_OBF", "rb") as f:
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
	
	tablePreprocessing = readTableBinkitPreprocessing()
	frameworksData = {}
	
	for nEmb in ELAPSED_SCs:
		SCs = 0
		N = 0
		for idS in ELAPSED_SCs[nEmb]:
			SCs += sum(ELAPSED_SCs[nEmb][idS])
			N += len(ELAPSED_SCs[nEmb][idS])				
		
		total  = SCs
		avg    = SCs/N
		
		f = nEmb.replace("PSSV16","PSSO")
		f = f.replace("SCG","ASCG")
		frameworksData[f] = {}
	
		if f in tablePreprocessing:
			total += tablePreprocessing[f]["Total"]
			avg   += tablePreprocessing[f]["Average"]
				
		frameworksData[f]["AVG"] = formatTimeAvg(avg)
		if f in tablePreprocessing:
			frameworksData[f]["AVG"] += " ("+formatTimeAvg(tablePreprocessing[f]["Average"])+ ")"						

		frameworksData[f]["Total"] = formatTime(total)
		if f in tablePreprocessing:
			frameworksData[f]["Total"] += " ("+formatTime(tablePreprocessing[f]["Total"]) + ")"
		
	
	tableWithGoodNames = {}
	
	for f in frameworksData:
		f2 = correctNames(f)
		tableWithGoodNames[f2] = {}
		for x in frameworksData[f]:
			tableWithGoodNames[f2][x] = frameworksData[f][x]

	#df = pd.DataFrame(tableWithGoodNames).T
	#df.fillna(0, inplace=True)		
	#print(df)
	
	return tableWithGoodNames

#readBinkitSpeedRQ1()
