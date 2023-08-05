#!/usr/bin/python3

import os

def idSToCorrect():
	return [5,6,12]


def readToCorrect():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])
	L = []
	with open(os.path.join(ABS_PATH, "samples.txt"), "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]			
			pathJson =  os.path.join(ABS_PATH, "json", str(idS)+".tmp0.json")
			compilerOption = path.split("/")[-2][-2:]
			if not(idS in idSToCorrect()):
				continue    
			L += [(idS,path,compilerOption,name, pathJson)]
	return L
