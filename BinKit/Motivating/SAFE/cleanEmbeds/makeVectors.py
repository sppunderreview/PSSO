import time
import numpy as np
from os.path import isfile, join, getsize
from pathlib import Path

import pickle

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

totalFunctions = 0
removed = 0

L = []
for path in Path('EMBEDS').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1]
	L += [(idS,pathString)]

vecById = {}
for (idS,path) in L:
    vecById[idS] = []
    
    with open(path,"rb") as f:
        functionsData = pickle.load(f)
    for idF in functionsData:
        nameSafe, embeds = functionsData[idF]
        if nameSafe in functionsRemoved[idS]:
            removed += 1
            continue
        totalFunctions += 1
        vecById[idS] += [(nameSafe, embeds)]

with open("vecById", 'wb') as f:
    pickle.dump(vecById, f)

print("Removed", removed)    
print("Functions", totalFunctions)

"""
Removed    64 321
Functions 997 202
"""
