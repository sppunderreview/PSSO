#!/usr/bin/python3


import os

def readAllSamples():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])
	L = []
	with open(os.path.join(ABS_PATH, "samples.txt"), "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]			
			pathJson = os.path.join(ABS_PATH, "json", str(idS)+".tmp0.json")
			version = path.split("/")[-2][-2:]
			L += [(idS,path,version,name, pathJson)]
	return L
	

def selectSamples(option):
	L = readAllSamples()
	LS = []
	for (idS,p,o,n,pJ) in L:
		if o == option:
			LS += [(idS,p,o,n,pJ)]
	return LS
	
def benchmarkBV(o0,o1):	
	return (selectSamples(o0),selectSamples(o1))
