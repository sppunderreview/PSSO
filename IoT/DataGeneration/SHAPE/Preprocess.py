from pathlib import Path

import networkx as nx
import numpy as np

import time
import pickle
import json
	
TODO = []
for path in Path('../DATA/jsons/').rglob('*.json*'):
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

		functionName = {}
		graphP = {}
		
		for f in data["functions"]:
			idFunction = "F_"+str(f["id"])
			functionName[idFunction] = f["name"]
			graphP[idFunction] = []
			
			for nextF in f["call"]:
				idNF = "F_"+str(nextF)
				graphP[idFunction] += [idNF]
		
		G = nx.Graph()
		for x in graphP:
			for y in graphP[x]:
				nameX = functionName[x]
				if not(y in functionName):
					continue
				nameY = functionName[y]
				if nameX == nameY:
					continue
				G.add_edge(nameX, nameY)

		E[idS] = np.array([G.number_of_nodes(), G.number_of_edges()])
	except Exception as e:
		print("Exception:", idS, e)

	j += 1		
	if j % 100 == 0:
		timePerElement = (time.time()-start)/j
		print(int((len(TODO)-j)*timePerElement), "s")

with open("SHAPE", "wb") as f:
	pickle.dump(E,f)
