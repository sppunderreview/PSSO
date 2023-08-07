from os.path import isfile, join, getsize
from pathlib import Path

L = []
for path in Path('MOTIVATING').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1]
	L += [(idS,pathString)]

for (idS, pathString) in L:
	idS = idS.replace("EGM_", "")
	programFunctions = []	
	with open(pathString, "r") as f:
		for l in f.readlines():            
			programFunctions += [l]
			
	with open("MO/"+idS+".json", "w") as f:
		for l in programFunctions:
			l = l.replace("\"fname\": \"","\"fname\": \""+idS+"_")
			f.write(l)
            
