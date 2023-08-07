import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

from random import seed, shuffle
from multiprocessing import Process



print("Enter number of cpu:") 
PN = int(input())
print("Enter the absolute path to IDApro v7.5 idat64 executable:") 
pathIda64 = input() # /home/tristan/idapro-7.5/idat64
print("Enter the absolute path to the 'ExtractBinaryIDA.py' script:") 
pathScript = input() # /home/tristan/Documents/Travail/These/Artefact/BinKiT/normal/DataGenerator/ExtractBinaryIDA.py


# Recover IDA into python3 mode
system("rm  "+pathIda64+"/python/use_python2")


def cleanIdaFiles(pathString):
	extToRemove = [".id0",".id1",".id2",".nam",".til",".i64"]
	for ext in extToRemove:
		targetFile = pathString+ext
		if isfile(targetFile):
			system("rm "+targetFile)

def extractDataFromProgram(goodware, myId, maxId):
	global pathIda64, pathScript
	L = []
	i = 0
	for pathString in goodware:
		if i % maxId == myId:
			L += [pathString]
		i += 1
		
	start = time.time()
	j = 0		
	for pathString in L:				
		fileName = pathString.split("/")[-1]
		command = pathIda64+" -A -S"+pathScript+" \""+pathString+"\""
		system(command)		
		outputPath = pathString+".tmp.json" 
		pathTobeMoved = "jsons/"+fileName+".tmp.json"
		if isfile(outputPath):
			system("mv "+outputPath+" "+pathTobeMoved)
		system("touch dones/"+fileName)
		cleanIdaFiles(pathString)
		#print(pathTobeMoved)
		j += 1		
		if j % 10 == 0:
			timePerElement = (time.time()-start)/j
			print(myId, int((len(L)-j)*timePerElement), "s")

if __name__ == '__main__':	
	dones = {}
	for path in Path('dones/').rglob('*'):
		pathString = str(path)
		nameFile = pathString.split("/")[-1]
		dones[nameFile] = True	

	goodware = []
	for path in Path('samples').rglob('*'):
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
	print(len(goodware))
	
	P = []
	for i in range(PN):
		p = Process(target=extractDataFromProgram, args=(goodware,i, PN))
		p.start()
		P += [p]
	for p in P:
		p.join()
	
	system("rm -r dones")
	system("mkdir dones")
	
