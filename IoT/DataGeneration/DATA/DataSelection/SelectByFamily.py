import pickle
import json
from pathlib import Path

families = ["gafgyt", "mirai", "tsunami"] #, "dnsamp", "hajime", "ddostf", "lightaidra", "pnscan", "skeeyah", "vpnfilter"]
familiesOcc = {}
for x in families:
    familiesOcc[x] = 0

downloadedMetadata = {}
for path in Path('metadata').rglob('*'):
	pathString = str(path)
	idS = pathString.split("/")[-1].split(".")[0]
	downloadedMetadata[idS] = True


kept = {}
for idS in downloadedMetadata:
	with open("metadata/"+idS+".json", "r") as f:
		l = f.readline().lower()

		for s in families:
			if s in l:
				familiesOcc[s] += 1
				kept[idS] = True

print(familiesOcc)
print(len(kept))

with open("selectedByFamily", "wb") as f:
	pickle.dump(kept, f)


"""
{'gafgyt': 9033, 'mirai': 23830, 'tsunami': 1951, 'dnsamp': 19, 'hajime': 55, 'ddostf': 33, 'lightaidra': 13, 'pnscan': 1, 'skeeyah': 29, 'vpnfilter': 6}
24870

{'gafgyt': 9033, 'mirai': 23830, 'tsunami': 1951}
24833
"""
