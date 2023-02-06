# ? ?
# ? 2022

import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

from random import seed, shuffle
from multiprocessing import Process


PN = 1 # Number of processors
pathIda64 = " /idapro-7.5/idat64" # Absolute path to the idat64 executable
pathScript = "ExtractBinaryViaIDA4.py" # Absolute path to the python ida script

def cleanIdaFiles(pathString):
	extToRemove = [".id0",".id1",".id2",".nam",".til",".i64"]
	for ext in extToRemove:
		targetFile = pathString+ext
		if isfile(targetFile):
			system("rm "+targetFile)
	 
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
		print(command)
		outputPath = pathString+".tmp.json" 
		pathTobeMoved = "jsons/"+fileName+".tmp.json"
		if isfile(outputPath):
			system("mv "+outputPath+" "+pathTobeMoved)
		cleanIdaFiles(pathString)
		
		j += 1		
		if j % 10 == 0:
			timePerElement = (time.time()-start)/j
			print(myId, int((len(L)-j)*timePerElement), "s")
			chunkNumber += 1


if __name__ == '__main__':
	dones = {}
	for path in Path('jsons').rglob('*'):
		pathString = str(path)
		if not(isfile(pathString)):
			continue
		idS = pathString.split("/")[-1].replace(".tmp.json","")
		dones[idS] = True
	
	print(len(dones))
	
	goodware = []		
	for path in Path('programs').rglob('*'):
		pathString = str(path)
		if ".id0" in pathString or ".id1" in pathString or ".id2" in pathString or ".nam" in pathString or ".til" in pathString or ".json" in pathString or ".i64" in pathString:
			continue
		if not(isfile(pathString)):
			continue
		nameFile = pathString.split("/")[-1]
		if nameFile in dones:
			continue
		goodware += [pathString]		

	# Deterministic shuffle of inputs
	goodware.sort()
	seed(10)
	shuffle(goodware)
	
	print(len(goodware)) # 4351
	
	P = []
	for i in range(PN):
		p = Process(target=extractDataFromProgram, args=(goodware,i, PN))
		p.start()
		P += [p]
	for p in P:
		p.join()
	
