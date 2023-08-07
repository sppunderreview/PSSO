import numpy as np
import pickle
from pathlib import Path

PSSV16 = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		PSSV16[idS] = pickle.load(f)

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

preprocessQPSSV16 = {}
for idS in Q:
	if idS in PSSV16:
		preprocessQPSSV16[idS] = PSSV16[idS][-1]

with open("preprocessQPSS16", "wb") as f:
	pickle.dump(preprocessQPSSV16, f)

