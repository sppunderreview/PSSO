import numpy as np
import pickle
from pathlib import Path

E = {}
preproQ = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		E[idS] = pickle.load(f)
		preproQ[idS] = E[idS][-1]

with open("PSSV16", "wb") as f:
	pickle.dump(E,f)

with open("preprocessQPSSO", "wb") as f:
	pickle.dump(preproQ,f)
	

