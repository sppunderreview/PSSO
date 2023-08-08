import pickle

embeds = ["preprocessQSCG","preprocessQPSSO","preprocessQPSS","MUTANTX2","PSSV16","PSS_D_5535","LIBDX","STRINGS","SCG_D_5535","FUNCTIONSET","SHAPE","BSIZE","DSIZE"]

with open("idS_Old_Version", "rb") as f:
	idSOV = pickle.load(f)

for n in embeds:
	with open("complete/"+n, "rb") as f:
		E = pickle.load(f)
	print(n, len(E))
	toRemove = []
	for idS in E:
		if idS in idSOV:
			continue
		toRemove += [idS]
	for idS in toRemove:
		del E[idS]
	print(n, len(E))
	with open("final/"+n, "wb") as f:
		pickle.dump(E,f)
	
	
	
