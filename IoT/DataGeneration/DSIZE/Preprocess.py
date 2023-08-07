import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

import numpy as np
import pickle

if __name__ == '__main__':
	goodware = []
	
	L =  [str(p) for p in Path('../DATA/jsons/').rglob('*')]
		
	for pathString in L:
		if not(isfile(pathString)) or not (".tmp.json" in pathString):
			continue
		idS = pathString.split("/")[-1]
		idS = idS.replace(".tmp.json" , "")
		sizeF = getsize(pathString)
		goodware += [(idS, sizeF, pathString)]		
	
	E = {}
	for (idS, sizeF, pathString) in goodware:
		E[idS] = np.array([sizeF])

	with open("DSIZE", "wb") as f:
		pickle.dump(E, f)
	
	print(len(E))
