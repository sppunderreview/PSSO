import numpy as np
import pickle
from pathlib import Path

preprocessQPSS = {}
for path in Path('Features').rglob("*"):
    idS = str(path).split("/")[-1]
    with open(path, "rb") as f:
        E = pickle.load(f)
        preprocessQPSS[idS] = (E[-1], len(E[0]))

with open("preprocessQPSS", "wb") as f:
    pickle.dump(preprocessQPSS,f)

