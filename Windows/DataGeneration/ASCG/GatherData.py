import numpy as np
import pickle
from pathlib import Path

E = {}
for path in Path('Features').rglob("*"):
	idS = str(path).split("/")[-1]
	with open(path, "rb") as f:
		E[idS] = pickle.load(f)[0]

with open("GSA", "wb") as f:
	pickle.dump(E,f)

