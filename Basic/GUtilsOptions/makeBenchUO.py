#!/usr/bin/python3

# ? ?
# 2021
# ?

def readAllSamples():
	L = []
	with open("C:\\Users\\?\\Desktop\\GUtilsOptions\\samples.txt", "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]			
			pathJson = "C:\\Users\\?\\Desktop\\GUtilsOptions\\json\\"+str(idS)+".tmp0.json"
			option = path.split("/")[-3][-2:]
			L += [(idS,path,option,name, pathJson)]
	return L
	

def selectSamples(option):
	L = readAllSamples()
	LS = []
	for (idS,p,o,n,pJ) in L:
		if o == option:
			LS += [(idS,p,o,n,pJ)]
	return LS
	
def benchmarkUO(o0,o1):	
	return (selectSamples(o0),selectSamples(o1))

