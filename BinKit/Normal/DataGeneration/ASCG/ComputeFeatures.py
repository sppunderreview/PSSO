import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import networkx as nx 
import time
import pickle
from pathlib import Path

from os.path import isfile

from LoadBase import loadGraphs

def makeGraph(lAdj):
	G = nx.Graph()
	for x in lAdj:
		for y in lAdj[x]:
			if x == y:
				continue
			G.add_edge(x, y)
	return G

def computeSpectrum(g):
	return -np.sort(-nx.spectrum.laplacian_spectrum(g))
	
def computeEmbeddings(toDo):
	startBS = time.time()
	u = 0
	for x in toDo:
		idS = x[0]
		outputFile = "Features/"+idS	
		try:		
			start = time.time()
			elapsedP, _, CallGraph = loadGraphs([x])
			elapsedP = elapsedP[idS]
			CallGraph = CallGraph[idS]
			
			# Call Graph spectrum normalized
			CallGraphSpectrum = computeSpectrum(makeGraph(CallGraph))			
			CallGraphSpectrum = CallGraphSpectrum/CallGraphSpectrum[0]
			
			elapsedPreprocessing = time.time() - start + elapsedP
			embedding =  [CallGraphSpectrum, elapsedPreprocessing]
			print(idS, len(CallGraphSpectrum), elapsedPreprocessing)

			with open(outputFile, "wb") as f:
				pickle.dump(embedding, f)
		except Exception as err:
			print("Exception:", idS, err)
			#with open(outputFile, "w") as f:
			#	pass

		u += 1
		if u % 100 == 0:			
			timeLeft = ((len(toDo) - u)/ 100) * (time.time()-startBS)
			print(u*100/len(toDo),"%", int(timeLeft), "s")
			startBS = time.time()


if __name__ == '__main__':
	goodware = []
	for path in Path('../jsons').rglob('*'):
		pathJson = str(path)
		goodware += [pathJson]
	
	toDo = []
	
	for pathJson in goodware:
		idS = pathJson.replace(".tmp.json","").split("/")[-1]
		outputFile = "Features/"+idS
		if isfile(outputFile) == True:
			continue
		toDo += [(idS, "?","?","?", pathJson)]

	print(len(toDo))
	computeEmbeddings(toDo)



