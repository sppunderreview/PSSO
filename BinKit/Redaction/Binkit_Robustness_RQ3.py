import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-1]))

import pandas as pd

from Binkit_Robustness_RQ3_Random import readBinkitRobustnessRQ3Random


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
	a = a.replace("LIBDX", "LibDX")
	return a
	
def readBinkitRobustnessRQ3():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    	
	testfields = {}


	with open(os.path.join(ABS_PATH, "RESULTS.txt"), "r") as f:
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

	for tf in testfields:
		for m in testfields[tf]:
			testfields[tf][m] =  sum(testfields[tf][m])/len(testfields[tf][m])
			testfields[tf][m] =  "{0:.2f}".format(testfields[tf][m])

	# Random choice
	randomResults = readBinkitRobustnessRQ3Random()
	
	for testfield in randomResults:
		st = testfield.split("_VS_")
		st = sorted(st)
		st = "_VS_".join(st)
		if st != testfield:
			testfields[st]["Random"] = "{0:.2f}".format((randomResults[testfield] + randomResults[st])/2)
		
	
	selected  = ["O0_VS_O1","O0_VS_O2","O0_VS_O3","O1_VS_O2","O1_VS_O3","O2_VS_O3", "gcc-4.9.4_VS_gcc-8.2.0", "clang-4.0_VS_clang-7.0", "clang_VS_gcc"]
	selected += ["clang-obfus-bcf_VS_normal","clang-obfus-fla_VS_normal","clang-obfus-sub_VS_normal","clang-obfus-all_VS_normal"]

	archs = ["arm","mips","x86"]
	for x in archs:
		for y in archs:
			if x >= y :
				continue
			selected += [x+"_VS_"+y]
	selected += ["32_VS_64"]
	testfieldsS = {}
	for x in selected:
		x2 = x.replace("_", " ")
		x2 = x2.replace("VS", "vs")
		x2 = x2.replace("4.9.4","4")
		x2 = x2.replace("8.2.0","8")
		x2 = x2.replace("4.0","4")   
		x2 = x2.replace("7.0","7")
		x2 = x2.replace("clang-obfus-","")
		x2 = x2.replace(" vs normal", "")
		testfieldsS[x2] = testfields[x]
	
	tableWithGoodNames = {}	
	for x in testfieldsS:
		tableWithGoodNames[x] = {}		
		for y in testfieldsS[x]:
			if y == "MUTANTX": # Old version of MUTANTX
				continue
			f = correctNames(y)
			tableWithGoodNames[x][f] = testfieldsS[x][y]
		
	df = pd.DataFrame(tableWithGoodNames)
	print("Table 8 (RQ2,RQ3) Precision scores on the BinKit dataset")
	print(df)
	
	return tableWithGoodNames

#readBinkitRobustnessRQ3()
