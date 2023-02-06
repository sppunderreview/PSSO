import os
from os.path import isfile
from pathlib import Path

import pickle
import numpy as np
			
with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)
    
T = 0
for idS in preprocessQPSS:
    T += preprocessQPSS[idS]

print(T/len(preprocessQPSS), T)


with open("preprocessQSCG", "rb") as f:
	preprocessQSCG = pickle.load(f)	
	
T = 0
for idS in preprocessQSCG:
    T += preprocessQSCG[idS]

print(T/len(preprocessQSCG), T)