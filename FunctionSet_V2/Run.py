from pathlib import Path
from random import shuffle

import time
import pickle
import json

def extractFunctionSetFromPrograms(L):
	start = time.time()
	j = 0
	for (pathJson, idS) in L:
		outputPath = "A_FUNCTIONSET/"+idS
		try:
			with open(pathJson, "r", encoding='latin1') as f:
				data = json.load(f)			
			externCalls = set()
			for f in data["functions"]:
				for nameCall in f["api"]:
					externCalls.add(nameCall)
			with open(outputPath,"wb") as f:
				pickle.dump(externCalls, f)
		except Exception as e:
			print(e)
			with open(outputPath, "w") as f:
				pass

		j += 1		
		if j % 100 == 0:
			timePerElement = (time.time()-start)/j
			print(int((len(L)-j)*timePerElement), "s")

done = {}
for path in Path('A_FUNCTIONSET/').rglob('*'):
	pathString = str(path)
	idS = pathString.split("/")[-1]
	idS = idS.replace(".tmp.json", "")
	done[idS] = True
	
TODO = []
for path in Path('../jsons/').rglob('*.json*'):
	pathString = str(path)
	nameFile = pathString.split("/")[-1]
	nameFile = nameFile.replace(".tmp.json", "")
	TODO += [(pathString, nameFile)]
	
TODOL = []
for (p, idS) in TODO:
	if idS in done:
		continue
	TODOL += [(p,idS)]
TODO = TODOL


print(len(done))
print(len(TODO))

extractFunctionSetFromPrograms(TODO)
