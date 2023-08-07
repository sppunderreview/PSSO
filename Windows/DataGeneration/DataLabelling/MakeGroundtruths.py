from copy import deepcopy
import time
from os import system
from os.path import isfile, join, getsize
from pathlib import Path

import pickle

L = [path for path in Path('../samples/').rglob('*')]

goodware = []
for path in L:
	pathString = str(path)
	if ".id0" in pathString or ".id1" in pathString or ".id2" in pathString or ".nam" in pathString or ".til" in pathString or ".json" in pathString or ".i64" in pathString:
		continue
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1]
	goodware += [idS]		

hexD = {}
for i in range(10):
	hexD[str(i)] = True
for a in ["a","b","c","d","e","f"]:
	hexD[a] = True
	
idSToName = {}
for idS in goodware:
	txt = idS
	while True:
		isHex = True
		for i in range(1,6):
			if not(txt[-i] in hexD):
				isHex = False
				break
		if isHex == False:
			break
		txt = txt[:-5]
		if txt[-1] in hexD:
			txt = txt[:-1]		
		if txt[-1] == "_":
			txt = txt[:-1]
	idSToName[idS] = txt

nameToIdS = {}
for idS in idSToName:
	name = idSToName[idS]
	if not(name in nameToIdS):
		nameToIdS[name] = []
	nameToIdS[name] += [idS]

print(len(nameToIdS))

with open("idSToName", "wb") as f:
	pickle.dump(idSToName, f)

with open("nameToIdS", "wb") as f:
	pickle.dump(nameToIdS, f)

