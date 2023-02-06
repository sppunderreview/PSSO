import pickle

with open("../Obfus/NORMAL_EMBEDS_2/BSIZE", "rb") as f:
    E = pickle.load(f)
    BN = [E[idS] for idS in E ]

with open("../Obfus/OBFUS_EMBEDS/BSIZE", "rb") as f:
    E = pickle.load(f)
    BO = [E[idS] for idS in E ]

SBN = sum(BN)/len(BN)
SBO = sum(BO)/len(BO)

SBN/= 1000
SBO/= 1000

print(SBN) # 201 Ko
print(SBO) # 514 Ko

SBG = sum(BN+BO)/(len(BN)+len(BO))
SBG/= 1000
print(SBG) # 313 Ko
