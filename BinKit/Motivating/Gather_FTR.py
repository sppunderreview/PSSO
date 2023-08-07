# Tristan Benoit
# These 2022
from os.path import isfile, join, getsize
from pathlib import Path

import pickle

L = []
for path in Path('FTM').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	L += [pathString]

FTR = []

for path in L:
	with open(path, "r") as f:
		t = f.readline().strip()
		t = t[1:-1]
		s = t.split(", ")
		FTR += s

print(len(FTR))
with open("FTRM", "wb") as f:
	pickle.dump(FTR, f)
	
