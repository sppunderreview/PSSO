import os
import pickle

with open("preprocessQPSS16", "rb") as f:
	preprocessQPSS = pickle.load(f)

for nQBI in [ "QB"]:
    with open(nQBI, "rb") as f:
        E = pickle.load(f) # [Q,B,I,QNames]
        Q = E[0]    
    P = []
    for idS in Q:
        if idS in preprocessQPSS:
            P += [preprocessQPSS[idS]]
    print(nQBI,sum(P)/len(P), sum(P))

"""
QB    0.39305151153939477 19430.50147294998
"""
