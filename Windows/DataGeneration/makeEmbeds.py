import os
from os.path import isfile
from pathlib import Path

import pickle
import json

import random
import time

import numpy as np
import networkx as nx

# PSS
# [SL, len(SL), traceF, len(traceF), elapsed]
def embeddingPSS(E):	
	return ( np.array(E[0]), np.array(E[2]) )

# SCG
# [spectrum, elapsed]
def embeddingSCG(E):	
	return np.array(E[0])

# Mutant-X
# {4-gram -> freq}
# (embedding,elasped)
def embeddingMUTANTX(E):
	D = E[0]	
	embed = [0 for i in range(4096)]	
	for ngram in D:
		t = ngram.replace("??", "ff")
		t = t.replace("-", "f")
		
		isBinary = True
		for c in t:
			if not(c in ["0","1", " "]):
				isBinary = False
				break
		t = t.split("_")
		t = [x for x in t if x != "" ]
		
		if isBinary:
			ngramInt = [ int(s, 2) for s in t]
		else:
			ngramInt = [ int(s, 16) for s in t]
		hashNgram = 7		
		for x in ngramInt:
			hashNgram = 31 * hashNgram + x
		p = hashNgram % 4096

		embed[p] += D[ngram]	
	return np.array(embed)


for (fEmb, nEmb) in  [(embeddingMUTANTX, "MUTANTX"),(None, "SHAPE"),(None, "FUNCTIONSET"),(embeddingSCG, "GSA"),(embeddingPSS, "PSS")]:
	print(nEmb)
	dT = {}
	for path in Path("../"+nEmb+"/A_"+nEmb+"/").rglob('*'):
		pathF = str(path)
		idS = pathF.split("/")[-1]
		try:	
			with open(pathF, "rb") as f:
				E = pickle.load(f)
		
			if fEmb != None:			
				E = fEmb(E)
			dT[idS] = E
		except Exception as e:
			if nEmb == "FUNCTIONSET":
				dT[idS] = set()
			else:
				print(e)
					
	with open(nEmb,"wb") as f:
		pickle.dump(dT, f)


