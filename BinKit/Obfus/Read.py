import pickle

ID_RUN = 1

#LC  = ["PSS","PSSV16", "SHAPE","BSIZE","DSIZE","SCG","STRINGS"]
LC = ["LIBDX"]
#LC += ["FUNCTIONSET","MUTANTX2"]

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QBs", "rb") as f:
    QBs = pickle.load(f)

for (nQBI, Q, B) in QBs:
    nQBI = nQBI.replace("/", "_VS_")
    for nEmb in LC:
        RESULTS = []
        for pId in range(40):
            inputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
            with open(inputFile, "rb") as f:
                RESULTS += pickle.load(f)
        ACC = []
        T = []
        for i in range(1,len(RESULTS), 3):
            ACC += [RESULTS[i]]
            T += [RESULTS[i+1]]
        S = sum(ACC)
        T = sum(T)
        print(nEmb, nQBI, S, len(ACC), S/len(ACC), T/len(ACC))