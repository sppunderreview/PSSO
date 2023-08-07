from pathlib import Path
from os.path import isfile, getsize

from Prototype import computeEmbedding
import pickle

if __name__ == '__main__':
	IoT = []
	for path in Path('../DATA/samples').rglob('*'):
		pathJson = str(path)
		idS = pathJson.split(".tmp.json")[0].split("../DATA/samples/")[1]
		IoT += [idS]

	embeds = computeEmbedding(IoT)
	with open("STRINGS", "wb") as f:
		pickle.dump(embeds, f)


