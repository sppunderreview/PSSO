import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

import numpy as np
import pickle

if __name__ == '__main__':
	L = [path for path in Path('../DATA/samples/').rglob('*')]
	
	goodware = []
	for path in L:
		pathString = str(path)
		if ".id0" in pathString or ".id1" in pathString or ".id2" in pathString or ".nam" in pathString or ".til" in pathString or ".json" in pathString or ".i64" in pathString:
			continue
		if not(isfile(pathString)):
			continue
		idS = pathString.split("/")[-1]
		sizeF = getsize(pathString)
		goodware += [(idS, sizeF, pathString)]		
	
	E = {}
	for (idS, sizeF, pathString) in goodware:
		E[idS] = np.array([sizeF])
		
	with open("BSIZE", "wb") as f:
		pickle.dump(E, f)
	
	print(len(E))
