import pickle

def formatTime(s):    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = round(s % 60)
    if h > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"
    
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

for nEmb in ELAPSED_SCs:
    SCs = 0
    N = 0
    for idS in ELAPSED_SCs[nEmb]:
        SCs += sum(ELAPSED_SCs[nEmb][idS])
        N += len(ELAPSED_SCs[nEmb][idS])
    print(nEmb, formatTime(SCs), N, SCs/N)

