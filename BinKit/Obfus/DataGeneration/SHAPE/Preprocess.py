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
		with open(pathJson, "r", encoding='latin1') as f:
			data = json.load(f)			

		graphP = {}
		for f in data["functions"]:
			idFunction = "F_"+str(f["id"])
			graphP[idFunction] = []
			
			for nextF in f["call"]:
				idNF = "F_"+str(nextF)
				graphP[idFunction] += [idNF]
		
		G = nx.Graph()
		for x in graphP:
			for y in graphP[x]:
				if x == y:
					continue
				G.add_edge(x, y)

		E[idS] = np.array([G.number_of_nodes(), G.number_of_edges()])
	except Exception as e:
		print("Exception:", idS, e)

	j += 1		
	if j % 100 == 0:
		timePerElement = (time.time()-start)/j
		print(int((len(TODO)-j)*timePerElement), "s")

with open("SHAPE", "wb") as f:
	pickle.dump(E,f)
