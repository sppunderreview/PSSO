import numpy as np
import pickle
from pathlib import Path

# ASCG
# E : [SpectrumCG, elapsed]
# Conversion for legacy stuff
# 5535 is the maximum number of nodes of a call graph in IoT dataset
def convertForCloneSearchASCG(E, D=5535):	
	l = []		
	for i in range(D):
		if i >= len(E[0]):
			l += [0]
			continue
		l += [ E[0][i] ]
	return np.array(l)

ASCG_ELAPSED_PREPRO = {}
ASCG_CLONE_SEARCH = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		E = pickle.load(f)
		
		ASCG_ELAPSED_PREPRO[idS] = E[-1]
		ASCG_CLONE_SEARCH[idS] = convertForCloneSearchASCG(E)

with open("preprocessQSCG", "wb") as f:
	pickle.dump(ASCG_ELAPSED_PREPRO,f)
	
with open("SCG_D_5535", "wb") as f:
	pickle.dump(ASCG_CLONE_SEARCH,f)

