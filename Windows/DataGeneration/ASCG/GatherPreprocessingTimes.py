import numpy as np
import pickle
from pathlib import Path

preprocessQSCG = {}
for path in Path('Features').rglob("*"):
    idS = str(path).split("/")[-1]
    with open(path, "rb") as f:
        E = pickle.load(f)
        preprocessQSCG[idS] = (E[-1], len(E[0]))

with open("preprocessQSCG", "wb") as f:
    pickle.dump(preprocessQSCG,f)

