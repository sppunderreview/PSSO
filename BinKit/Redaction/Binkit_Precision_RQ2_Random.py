import os

import pickle

def randomPrecision(QBs, T):
	RESULTS = []
	for QB in QBs:
		(_, Q, B)  = QB

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
		RESULTS += [sum(p)/len(p)]
	return RESULTS


def readBinkitPrecisionRQ2Random():
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

	RESULTS += randomPrecision(QBs, T)
	
	return sum(RESULTS)/len(RESULTS)

#print(readBinkitPrecisionRQ2Random())
