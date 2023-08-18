import os
import pickle

def randomPrecision(Q, B, T):
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
	return sum(p)/len(p)


def readWindowsPrecisionRQ2Random():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	with open(os.path.join(ABS_PATH, "QB"), "rb") as f:
		QB = pickle.load(f)
		Q = QB[0]
		B = QB[1]

	with open(os.path.join(ABS_PATH, "idSToName"), "rb") as f:
		T = pickle.load(f)

	return randomPrecision(Q, B, T)


#print(readWindowsPrecisionRQ2Random())
