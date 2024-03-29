import pickle

ID_RUN = 1

LC  = ["simCG", "simCFG"]

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QBs", "rb") as f:
    QBs = pickle.load(f)
with open("QBAs", "rb") as f:
    QBs += pickle.load(f)
    
ELAPSED_SCs_NORMAL = {}

for (nQBI, Q, B) in QBs:
    nQBI = nQBI.replace("/", "_VS_")
    for nEmb in LC:
        if not (nEmb in ELAPSED_SCs_NORMAL):
            ELAPSED_SCs_NORMAL[nEmb] = {}    
        RESULTS = []
        for pId in range(40):
            inputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
            with open(inputFile, "rb") as f:
                RESULTS += pickle.load(f)
        

        for i in range(1,len(RESULTS), 3):
            idS =  RESULTS[i-1]            
            if not(idS) in ELAPSED_SCs_NORMAL[nEmb]:
                ELAPSED_SCs_NORMAL[nEmb][idS] = []
            ELAPSED_SCs_NORMAL[nEmb][idS] += [RESULTS[i+1]]
            
with open("ELAPSED_SCs_Ablation_NORMAL", "wb") as f:
    pickle.dump(ELAPSED_SCs_NORMAL,f)