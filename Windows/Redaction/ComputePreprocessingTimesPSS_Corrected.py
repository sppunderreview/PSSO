import os
from pathlib import Path
from os.path import isfile
import pickle

with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)

with open("preprocessQSCG", "rb") as f:
	preprocessQSCG = pickle.load(f)
    
with open("SPECTRUM_PREPROCESSING_PSS_CORRECTED", "rb") as f:
	SPECTRUM_PSSC = pickle.load(f)

# Correct runnting times:
for idS in preprocessQPSS:
	if preprocessQPSS[idS][1] > 50000:
		preprocessQPSS[idS] = [SPECTRUM_PSSC[idS][1], preprocessQPSS[idS][1]]

for idS in preprocessQSCG:
	if preprocessQPSS[idS][1] > 50000:
		preprocessQSCG[idS] = [SPECTRUM_PSSC[idS][1], preprocessQSCG[idS][1]]

LC =  ["PSS","GSA"]

for nEmb in LC:
    LATEX = ""
    for nQBI in ["QB"]:
        with open(nQBI, "rb") as f:
            E = pickle.load(f) # [Q,B,I,QNames]
            Q = E[0]
        
        if nEmb == "PSS":
            P = []
            for idS in Q:
                P += [preprocessQPSS[idS][0]]
            PMeans = sum(P)/len(P)
        elif nEmb == "GSA":
            P = []
            for idS in Q:
                P += [preprocessQSCG[idS][0]]
            PMeans = sum(P)/len(P)
        else:
            PMeans = 0

        LATEX +=  "%.2f" % (PMeans) + " & "
        print(sum(P))
        
    print(nEmb)    
    print(LATEX)

"""
838042.923987627
PSS
16.95 &
820586.7117142677
GSA
16.60 &
"""

