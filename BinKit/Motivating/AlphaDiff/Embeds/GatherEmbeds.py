from pathlib import Path
from os.path import isfile

import pickle

# Gather
vecById = {}
for path in Path('EMBEDS').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1]
	with open(pathString,"rb") as f:
		vecById[idS] = pickle.load(f)

with open("vecById","wb") as f:
	pickle.dump(vecById,f)
		
	
