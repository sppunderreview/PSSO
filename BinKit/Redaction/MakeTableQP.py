import pickle

with open("ELAPSED_SCs_NORMAL", "rb") as f:
    ELAPSED_SCs_NORMAL  = pickle.load(f)

with open("ELAPSED_SCs_OBF", "rb") as f:
    ELAPSED_SCs_OBF = pickle.load(f)

print([x for x in ELAPSED_SCs_NORMAL])
print([x for x in ELAPSED_SCs_OBF])

ELAPSED_SCs = ELAPSED_SCs_NORMAL

for nEmb in ELAPSED_SCs_OBF:    
    for idS in ELAPSED_SCs_OBF[nEmb]:
        if not(idS in ELAPSED_SCs[nEmb]):
            ELAPSED_SCs[nEmb][idS] = ELAPSED_SCs_OBF[nEmb][idS]
        else:
            ELAPSED_SCs[nEmb][idS] += ELAPSED_SCs_OBF[nEmb][idS]

QP_EMBS = {}
for nEmb in ["PSS", "SCG","PSSV16"]:
    QP_EMBS[nEmb] = {}
    with open("../Obfus/NORMAL_EMBEDS_2/"+nEmb, "rb") as f:
        E = pickle.load(f)
        for idS in  E:
            QP_EMBS[nEmb][idS] = E[idS][-1]
    with open("../Obfus/OBFUS_EMBEDS/"+nEmb, "rb") as f:
        E = pickle.load(f)
        for idS in  E:
            QP_EMBS[nEmb][idS] = E[idS][-1]

        
for nEmb in ["PSS", "SCG","PSSV16"]:
    QPs = 0
    N = 0
    for idS in ELAPSED_SCs[nEmb]:
        QPs += QP_EMBS[nEmb][idS] * len(ELAPSED_SCs[nEmb][idS])
        N += len(ELAPSED_SCs[nEmb][idS])
    print(nEmb, QPs, N, QPs/N)

"""
% QP PSS: 292313.92229390144 1391184 0.21011880692554072
% QP PSS_O: 50601.60943365097 1391184 0.03637305304952542
% QP ASCG: 292270.14190387726 1391184 0.21008733704806642
"""