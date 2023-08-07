import numpy as np
import pickle
from pathlib import Path

# PSS
# E : [SpectrumCG, len(), edgesCFG, len(), elapsed]
# Conversion for legacy stuff
# 5535 is the maximum number of nodes of a call graph in IoT dataset
def convertForCloneSearchPSS(E, D=5535):
	l = []		
	for i in range(D):
		if i >= E[1]:
			l += [0]
			continue
		l += [ E[0][i] ]

	for i in range(D):
		if i >= E[-2]:
			l += [0]
			continue
		l += [ E[2][i] ]

	return np.array(l)


PSS_ELAPSED_PREPRO = {}
PSS_CLONE_SEARCH = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		E = pickle.load(f)
		
		PSS_ELAPSED_PREPRO[idS] = E[-1]
		PSS_CLONE_SEARCH[idS] = convertForCloneSearchPSS(E)		

with open("preprocessQPSS", "wb") as f:
	pickle.dump(PSS_ELAPSED_PREPRO,f)

with open("PSS_D_5535", "wb") as f:
	pickle.dump(PSS_CLONE_SEARCH,f)
