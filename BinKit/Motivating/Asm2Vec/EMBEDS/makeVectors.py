import time
import numpy as np
import pickle

from pathlib import Path
from os.path import isfile

# Load FTR
functionsRemoved = {} 
with open("FTRM", "rb") as f:
    FTRM = pickle.load(f)
for nameAsm2vec in FTRM:
	# "gmp-6.1.2_gcc-4.9.4_x86_32_O3_libgmp.so.10.3.2.elf_nl_langinfo_6534673368806049490"
    t2 = nameAsm2vec.split(".elf_")
    idS = t2[0]+".elf"
    nameSafe = "_".join(nameAsm2vec.split("_")[:-1])    
    if not(idS in functionsRemoved):
        functionsRemoved[idS] = {}
    functionsRemoved[idS][nameSafe] = True
    print(nameSafe)
        
print(sum([ len(functionsRemoved[idS]) for idS in functionsRemoved]))


# Gather
vecById = {}
removed = 0
totalF = 0

for path in Path('experiment_motivating').rglob('*'):
    pathString = str(path)
    if not(isfile(pathString)):
        continue
		
    vectorsbd = {}
    with open(pathString, "r") as f:
        EPOCHS = f.readline().strip()
        LR = f.readline().strip()
        RATIOET = f.readline().strip()
        nF = f.readline()
        while nF != "":
            nF = nF.strip()
            v = []
            for j in range(200):
                v+= [float(f.readline().strip())]
            vectorsbd[nF] = np.array(v)
            nF = f.readline()

    for v in vectorsbd:
        p = v.split(".elf")[0]+".elf"
        if not(p in vecById):
            vecById[p] = []
        nameSafe = "_".join(v.split("_")[:-1])   
        if nameSafe in functionsRemoved[p]:
            removed += 1
            continue
        vecById[p] += [vectorsbd[v]]
        totalF += 1

with open("vecById", 'wb') as f:
    pickle.dump(vecById, f)

print(len(vecById))	
print("functions", totalF)
print("removed", removed)


"""
"""
