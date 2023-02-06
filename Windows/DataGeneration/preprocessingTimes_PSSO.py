import pickle
import numpy as np

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

preprocessQPSS = {}
with open("PSSV16", "rb") as f:
    PSS16 = pickle.load(f)
for idS in Q:
    if idS in PSS16:
        preprocessQPSS[idS] = PSS16[idS][-1]
with open("preprocessQPSS16", "wb") as f:
	pickle.dump(preprocessQPSS, f)

