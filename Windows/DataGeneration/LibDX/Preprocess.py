from pathlib import Path
from os.path import isfile, getsize

from Prototype import computeEmbedding
import pickle

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
    
	embeds, featuresID = computeEmbedding(goodware)
	with open("LIBDX", "wb") as f:
		pickle.dump(embeds, f)

	with open("LIBDX_FEATURESID", "wb") as f:
		pickle.dump(featuresID, f)

	print(len(featuresID))
