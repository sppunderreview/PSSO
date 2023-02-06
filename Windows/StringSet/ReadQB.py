import os
import pickle

# RESULTS += [idSI, nameI == T[idMinJ], elapsed]

ID_RUN = 3
P = 80
nQBI = "QB"
nEmb = "STRINGS"

RESULTS = []
for pId in range(P):
   for RUN in ["","2","3"]:
       inputFile = "R/R"+RUN+"_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
       if os.path.isfile(inputFile):
           with open(inputFile, "rb") as f:
               RESULTS += pickle.load(f)
ACC = {}
T = {}
for i in range(0,len(RESULTS),3):
   ACC[RESULTS[i]] = RESULTS[i+1]
   T[RESULTS[i]] =  RESULTS[i+2]

S = 0
ST = 0
for idS in ACC:
   S += ACC[idS]
   ST += T[idS]
print(nEmb, nQBI, S, len(ACC), S/len(ACC), ST/len(T), ST)

# STRINGS QB 24774 49443 0.5010618287725259 18.470189909163174 913221.5996787548