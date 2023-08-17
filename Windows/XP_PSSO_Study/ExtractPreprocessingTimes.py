import pickle

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

for nEmb in ["PSSO_30","PSSO_50","PSSO_80","PSSO_130","PSSO_150","PSSO_180"]:
	with open("EMBEDS/"+nEmb, "rb") as f:
		E = pickle.load(f)
		P = {}
		for idS in E:
			P[idS] = E[idS][-1]

	with open("Prepro_"+nEmb, "wb") as f:
		pickle.dump(P,f)
