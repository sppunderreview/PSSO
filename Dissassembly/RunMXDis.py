# ? ?
# ? 2022

import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

from random import seed, shuffle
from multiprocessing import Process


PN = 1 # Number of processors
pathIda64 = " idat64" # Absolute path to the idat64 executable
pathScript = "ExtractBytesViaIDA.py" # Absolute path to the python ida script
archiveSizes  = 10 # Number of json files in an archive

def cleanIdaFiles(pathString):
	extToRemove = [".id0",".id1",".id2",".nam",".til",".i64"]
	for ext in extToRemove:
		targetFile = pathString+ext
		if isfile(targetFile):
			system("rm "+targetFile)
	
def compressJsons(L, idP, chunkNumber):
	X = ["jsons/"+pathString.split("/")[-1]+"_bytes.json" for pathString in L]
	X = [x for x in X if isfile(x)]
	outputPath = "chunksMX/jsons_"+str(idP)+"_"+str(chunkNumber)+".zip"	
	command = "zip -q "+outputPath+" "+" ".join(X)
	system(command)	
	for x in X:
		system("rm "+x)
	 
def extractDataFromProgram(goodware, myId, maxId):
	global pathIda64, pathScript, archiveSizes
	L = []
	i = 0
	for pathString in goodware:
		if i % maxId == myId:
			L += [pathString]
		i += 1
		
	start = time.time()
	j = 0
	chunkNumber = 0
		
	for pathString in L:				
		fileName = pathString.split("/")[-1]
		command = pathIda64+" -A -S"+pathScript+" \""+pathString+"\""
		system(command)
		outputPath = pathString+"_bytes.json" 
		pathTobeMoved = "jsons/"+fileName+"_bytes.json"
		if isfile(outputPath):
			system("mv "+outputPath+" "+pathTobeMoved)
		system("touch dones/"+fileName)
		cleanIdaFiles(pathString)
		
		j += 1		
		if j % archiveSizes == 0:
			timePerElement = (time.time()-start)/j
			print(myId, int((len(L)-j)*timePerElement), "s")
			compressJsons(L[j-archiveSizes:j], myId, chunkNumber)
			chunkNumber += 1
	compressJsons(L, myId, chunkNumber)

if __name__ == '__main__':
	dones = {}
	for path in Path('dones/').rglob('*'):
		pathString = str(path)
		nameFile = pathString.split("/")[-1]
		dones[nameFile] = True

	goodware = []
	for path in Path('normal_dataset').rglob('*'):
		pathString = str(path)
		if ".id0" in pathString or ".id1" in pathString or ".id2" in pathString or ".nam" in pathString or ".til" in pathString or ".json" in pathString or ".i64" in pathString:
			continue
		if not(isfile(pathString)):
			continue
		nameFile = pathString.split("/")[-1]
		if nameFile  in dones:
			continue
		goodware += [pathString]		

	# Deterministic shuffle of inputs
	goodware.sort()
	seed(10)
	shuffle(goodware)
	
	print(len(goodware)) # 67 680
	
	P = []
	for i in range(PN):
		p = Process(target=extractDataFromProgram, args=(goodware,i, PN))
		p.start()
		P += [p]
	for p in P:
		p.join()
	
