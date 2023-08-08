import pickle

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

with open("Preproccesing_EMBEDS", "wb") as f:
	pickle.dump(QP_EMBS, f)

