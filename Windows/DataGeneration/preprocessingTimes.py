import pickle
import numpy as np

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

preprocessQPSS = {}
preprocessQSCG = {}

for idS in B:
	with open("../PSS/A_PSS/"+idS, "rb") as f:
		E = pickle.load(f)
		preprossPSS = E[-1]
	preprocessQPSS[idS] = (preprossPSS, len(E[0]))

for idS in B:	
	with open("../GSA/A_GSA/"+idS, "rb") as f:
		E = pickle.load(f)
		preprossSCG = E[-1]
	preprocessQSCG[idS] = (preprossSCG, len(E[0]))
	
with open("preprocessQPSS", "wb") as f:
	pickle.dump(preprocessQPSS, f)

with open("preprocessQSCG", "wb") as f:
	pickle.dump(preprocessQSCG, f)
	
	
