import pickle

with open("idSToName", "rb") as f:
	idSToName = pickle.load(f)

with open("nameToIdS", "rb") as f:
	nameToIdS = pickle.load(f)

# Remove samples not treated by every framework
idSRemoved = {}

for framework in ["BSIZE","DSIZE","MUTANTX","PSS","GSA","FUNCTIONSET","SHAPE"]:
	with open(framework, "rb") as f:
		D =  pickle.load(f)

	for idS in idSToName:
		if not(idS in D):
			idSRemoved[idS] = True

for idS in idSRemoved:
	del idSToName[idS]

Q = {}
QNames = {}


# Add samples who have a clone
for n in nameToIdS:
	L = []
	for idS in nameToIdS[n]:
		if idS in idSToName:
			L += [idS] 
	if len(L) > 1:
		for idS in L:
			Q[idS] = True
		QNames[n] = len(L)
		
B = {}
for idS in idSToName:
	B[idS] = True
	
I = {}
for idS in B:
	if not(idS) in Q:
		I[idS] = True

print(len(Q))
print(len(B))
print(len(I))

with open("QB", "wb") as f:
	pickle.dump([Q,B,I,QNames], f)
