from pathlib import Path

import networkx as nx
import numpy as np

import time
import pickle
import json
	
TODO = []
for path in Path('../jsons/').rglob('*.json*'):
	pathString = str(path)
	idS = pathString.split("/")[-1]
	idS = idS.replace(".tmp.json", "")
	TODO += [(pathString, idS)]

E = {}

start = time.time()
j = 0
for (pathJson, idS) in TODO:
	try:
		with open(pathJson, "r") as f:
			data = json.load(f)			
		externCalls = set()
		for f in data["functions"]:
			for nameCall in f["api"]:
				externCalls.add(nameCall)
		E[idS] = externCalls
	except Exception as e:
		print("Exception:", idS, e)

	j += 1		
	if j % 100 == 0:
		timePerElement = (time.time()-start)/j
		print(int((len(TODO)-j)*timePerElement), "s")

with open("FUNCTIONSET", "wb") as f:
	pickle.dump(E,f)
