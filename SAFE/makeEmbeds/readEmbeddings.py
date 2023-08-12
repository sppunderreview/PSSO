import pickle
import numpy as np
from matplotlib import pyplot as plt

embeds = {}
for idS in range(348):
	with open("CV/"+str(idS), "rb") as f:
		embeds[idS] =pickle.load(f)

F = {}

for idS in embeds:
	for idF in embeds[idS]:
		(nF, X) = embeds[idS][idF]
		if not(nF in F):
			F[nF] = []
		F[nF] += [X]

print("# of unique function names:", len(F))

for nF in F:
	print("Function:", nF)
	print("Inside", len(F[nF]), "programs of Coreutils Versions")
	Y = np.concatenate(F[nF])
	plt.imshow(Y, interpolation='nearest')
	plt.title("Embeddings for "+nF)
	plt.show()
     

