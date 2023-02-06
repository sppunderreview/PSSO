#!/usr/bin/python3

# ? ?
# 2021
# ?

def readAllSamples():
	L = []
	with open("C:\\Users\\?\\Desktop\\GCoreutilsVersions\\samples.txt", "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]
			pathJson = "C:\\Users\\?\\Desktop\\GCoreutilsVersions\\json\\"+str(idS)+".tmp0.json"
			txtP = len("binaries/coreutils-")
			version = int(path[txtP:txtP+1]) - 5
			versionT = "V" + str(version)
			L += [(idS,path,versionT,name, pathJson)]
	return L
	

def selectSamples(option):
	L = readAllSamples()
	LS = []
	for (idS,p,o,n,pJ) in L:
		if o == option:
			LS += [(idS,p,o,n,pJ)]
	return LS
	
def benchmarkCV(o0,o1):	
	return (selectSamples(o0),selectSamples(o1))