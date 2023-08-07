from pathlib import Path
from os.path import isfile

from Prototype import computeEmbedding

# collect files
goodware = []
for path in Path('../../jsons').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1].replace(".tmp.json", "")
	t = idS.split("_")	
	arch = t[2]
	bits = int(t[3])

	if arch != "x86":
		continue		
	goodware += [(idS,"","","", pathString)]

computeEmbedding(goodware)
    
