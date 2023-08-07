from os.path import isfile, join, getsize
from pathlib import Path

import numpy as np
import pickle


# Load FTR
functionsRemoved = {} 
with open("FTRM", "rb") as f:
    FTRM = pickle.load(f)
for nameAsm2vec in FTRM:
	# "gmp-6.1.2_gcc-4.9.4_x86_32_O3_libgmp.so.10.3.2.elf_nl_langinfo_6534673368806049490"
    t2 = nameAsm2vec.split(".elf_")
    idS = t2[0]+".elf"
    nameSafe = "_".join(t2[1].split("_")[:-1])    
    if not(idS in functionsRemoved):
        functionsRemoved[idS] = {}
    functionsRemoved[idS][nameSafe] = True

# Gather
vecById = {}
for path in Path('vecById').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	with open(pathString,"rb") as f:
		vecByIdS = pickle.load(f)
		for idS in vecByIdS:
			vecById[idS] = vecByIdS[idS]


# Remove functions
totalFunctions = 0
removed = 0
vecByIdCleaned = {}
for idS in vecById:
	vecByIdCleaned[idS] = []
	for nameGemini in vecById[idS]:
		nameAsm2vec = nameGemini.split(".elf.json_")[1]    
		embeds = vecById[idS][nameGemini]
		if nameAsm2vec in functionsRemoved[idS]:
			removed += 1
			continue
		totalFunctions += 1
		vecByIdCleaned[idS] += [(nameAsm2vec, embeds)]

with open("vecByIdC", 'wb') as f:
	pickle.dump(vecByIdCleaned, f)

print("Removed", removed)    
print("Functions", totalFunctions)

"""
Removed    70 849
Functions 882 655
"""
