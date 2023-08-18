import os

import pickle

def randomPrecision(QBs, T):
	RESULTS = {}
	for QB in QBs:
		(nTF, Q, B)  = QB
		nTF = nTF.replace("/","_VS_")
		counterNamesInB = {}
		for idSJ in B:
			name = T[idSJ]
			if not(name in counterNamesInB):
				counterNamesInB[name] = 0
			counterNamesInB[name] += 1
			
		p = []
		for idSI in Q:
			counter = counterNamesInB[T[idSI]] - 1			
			p += [counter/(len(B)-1)]
		RESULTS[nTF] = sum(p)/len(p)
	return RESULTS


def readBinkitRobustnessRQ3Random():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	with open(os.path.join(ABS_PATH, "../Normal/QBs"), "rb") as f:
		QBs = pickle.load(f)
	with open(os.path.join(ABS_PATH, "../Normal/QBAs"), "rb") as f:
		QBs += pickle.load(f)
	with open(os.path.join(ABS_PATH, "../Normal/T"), "rb") as f:
		T = pickle.load(f)
	
	RESULTS = randomPrecision(QBs, T)

	with open(os.path.join(ABS_PATH, "../Obfus/QBs"), "rb") as f:
		QBs = pickle.load(f)
	with open(os.path.join(ABS_PATH, "../Obfus/T"), "rb") as f:
		T = pickle.load(f)

	RESULTS.update(randomPrecision(QBs, T))
	return RESULTS

