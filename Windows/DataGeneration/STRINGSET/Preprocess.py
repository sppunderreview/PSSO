from pathlib import Path
from os.path import isfile, getsize

from Prototype import computeEmbeddings
import pickle

import time
from random import shuffle

if __name__ == '__main__':
	L = [path for path in Path('../samples/').rglob('*')]
	
	goodware = []
	for path in L:
		pathString = str(path)
		if ".id0" in pathString or ".id1" in pathString or ".id2" in pathString or ".nam" in pathString or ".til" in pathString or ".json" in pathString or ".i64" in pathString:
			continue
		if not(isfile(pathString)):
			continue
		idS = pathString.split("/")[-1]
		goodware += [(idS, pathString)]		
    
	start = time.time()
	shuffle(goodware)
	computeEmbeddings(goodware)
	print(time.time()-start)
