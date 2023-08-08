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


def readBinkitPrecisionRQ2():
	testfields = {}

	with open("RESULTS.txt", "r") as f:
		for l in f.readlines():
			t = l.split(" ")
			m = t[0]        
			testfield = t[1]        
			st = testfield.split("_VS_")
			st = sorted(st)
			st = "_VS_".join(st)       
			acc = float(t[4])
			elapsed = float(t[5].strip())
			
			if not(st in testfields):
				testfields[st] = {}
			if not(m in testfields[st]):
				testfields[st][m] = []
			testfields[st][m] += [acc]  
			#SHAPE clang-7.0_VS_clang-4.0 4859 7520 0.6461436170212767 0.026812818487907977

	frameworkPlot = {}

	averageSI = {}
	for tf in testfields:
		for m in testfields[tf]:
			if not (m in averageSI):
				averageSI[m] = []
				
			if len(testfields[tf][m]) != 2:
				print("ALERT")
				
			testfields[tf][m] =  sum(testfields[tf][m])/len(testfields[tf][m])
			averageSI[m] += [testfields[tf][m]]
			testfields[tf][m] =  "{0:.2f}".format(testfields[tf][m])
	
	for m in averageSI:
		if m == "MUTANTX":
			continue
		score = sum(averageSI[m])/len(averageSI[m])
		m = correctNames(m)
		frameworkPlot[m] = {}
		frameworkPlot[m]["AVG"] = "{:.3f}".format(score)
		
	#df = pd.DataFrame(frameworkPlot).T
	#df.fillna(0, inplace=True)
	#print(df)	
	return frameworkPlot

#readBinkitPrecisionRQ2()
