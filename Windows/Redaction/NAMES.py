import pickle
with open("idSToName", "rb") as f:
	idSToName = pickle.load(f)
    
for idS in idSToName:
    print(idSToName[idS])
    