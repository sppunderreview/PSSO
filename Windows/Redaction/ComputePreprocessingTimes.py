import os
import pickle

with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)

with open("preprocessQSCG", "rb") as f:
	preprocessQSCG = pickle.load(f)

# Adjust runnting times:
# because for PSS preprocessing some very large programs were run with multiple processors
# , depending on number of nodes, a coefficient is applied to recover a comparable runtime
for idS in preprocessQPSS:
	if preprocessQPSS[idS][1] > 60000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 6, preprocessQPSS[idS][1]]
	elif preprocessQPSS[idS][1] > 50000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 3, preprocessQPSS[idS][1]]

for idS in preprocessQSCG:
	if preprocessQSCG[idS][1] > 60000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 6, preprocessQSCG[idS][1]]
	elif preprocessQSCG[idS][1] > 50000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 3, preprocessQSCG[idS][1]]	

LC =  ["PSS","GSA"]

for nEmb in LC:
    LATEX = ""
    for nQBI in [ "QB"]:
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

        LATEX +=  "%.2f" % (sum(P)) + " & "
        
        
    print(nEmb)    
    print(LATEX)

"""
PSS
162490.16 &
ASCG
157674.07 &
"""


