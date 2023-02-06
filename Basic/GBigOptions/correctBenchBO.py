#!/usr/bin/python3

# ? ?
# 2022
# ?

def idSToCorrect():
	return [5,6,12]


def readToCorrect():
	L = []
	with open("C:\\Users\\?\\Desktop\\GBigOptions\\samples.txt", "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]			
			pathJson = "C:\\Users\\?\\Desktop\\GBigOptions\\json\\"+str(idS)+".tmp0.json"
			compilerOption = path.split("/")[-2][-2:]
			if not(idS in idSToCorrect()):
				continue    
			L += [(idS,path,compilerOption,name, pathJson)]
	return L