import os
import pickle

with open("preprocessQPSS16", "rb") as f:
	preprocessQPSS = pickle.load(f)

for nQBI in [ "QB","QB40k", "QB20K"]:
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
QB40k 0.3828675242647826 9563.26502108574
QB20K 0.38622554943261556 4665.604637145996
"""
