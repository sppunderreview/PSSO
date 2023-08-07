from pathlib import Path
from os.path import isfile, getsize

from Prototype import computeEmbeddings
import pickle

import time
from random import shuffle

from tqdm import tqdm

# Optimize memory by replacing each unique string by an id

if __name__ == '__main__':
	L = [str(path) for path in Path('Features/').rglob('*')]	
	E = {}

	featuresId = 0
	featuresMap = {}
	
	for pathBlock in tqdm(L):
		with open(pathBlock, "rb") as f:
			B = pickle.load(f)
		
		for idS in B:
			stringMultiSet = B[idS][0]
			stringMultiSetEncoded = {}
			for s in stringMultiSet:
				if not (s in featuresMap):
					featuresMap[s] = featuresId
					featuresId += 1
				stringMultiSetEncoded[featuresMap[s]] = stringMultiSet[s]
			E[idS] = [stringMultiSetEncoded, B[idS][1]]

	with open("STRINGS", "wb") as f:
		pickle.dump(E,f)

	
