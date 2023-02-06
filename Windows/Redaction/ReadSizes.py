import pickle

with open("BSIZE", "rb") as f:
    E = pickle.load(f)
    BN = [E[idS] for idS in E ]

SBN = sum(BN)/len(BN)
SBN/= 1000
print(SBN) # 771 Ko
