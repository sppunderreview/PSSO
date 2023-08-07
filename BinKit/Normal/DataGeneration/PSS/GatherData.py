import numpy as np
import pickle
from pathlib import Path

E = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		x = pickle.load(f)
		E[idS] = [x[0],x[2],x[-1]]

with open("PSS", "wb") as f:
	pickle.dump(E,f)



