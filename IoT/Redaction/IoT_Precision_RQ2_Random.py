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


def readIoTPrecisionRQ2Random():
	ABS_PATH = "/".join(os.path.abspath(__file__).split("/")[:-1])    

	with open(os.path.join(ABS_PATH, "../MutantXSV2_PSSO/EMBEDS/PSSV16"), "rb") as f:
		E = pickle.load(f)

	with open(os.path.join(ABS_PATH, "../MutantXSV2_PSSO/LABELS"), "rb") as f:
		T = pickle.load(f)

	Q = [idS for idS in E]
	B = [idS for idS in E]
	
	return randomPrecision(Q, B, T)
	
	
#print(readIoTPrecisionRQ2Random())
