import pickle
import pandas as pd


def correctNames(a):
	a = a.replace("PSSV16", "PSSO")
	return a

def formatTime(s):	
	h = int(s / 3600)
	m = int((s - (h*3600))/ 60)
	s = round(s % 60)
	if h > 0:	
		return str(h)+"h"+str(m)+"m"
	if m > 0:
		return str(m)+"m"+str(s)+"s"
	return str(s)+"s"

def formatTimeAvg(s):	
	h = int(s / 3600)
	m = int((s - (h*3600))/ 60)
	s = s % 60
	if h == 0 and m == 0:
		s = round(s,2)
	else:
		s = round(s)
	if h > 0:	
		return str(h)+"h"+str(m)+"m"
	if m > 0:
		return str(m)+"m"+str(s)+"s"
	return str(s)+"s"

# SHARED REPOSITORIES & GROUND TRUTHS
with open("QBs", "rb") as f:
    QBs = pickle.load(f)

(nQBI, Q, B) = QBs[0]
nQBI = nQBI.replace("/", "_VS_")

print("MutantX-S results only on", nQBI, "in one direction.")

ID_RUN = 1
nEmb = "MUTANTX2"
RESULTS = []
for pId in range(1):
	inputFile = "RS/R_"+nQBI+"_"+nEmb+"_"+str(pId)+"_"+str(ID_RUN)
	with open(inputFile, "rb") as f:
		RESULTS += pickle.load(f)
ACC = []
T = []
for i in range(1,len(RESULTS), 3):
	ACC += [RESULTS[i]]
	T += [RESULTS[i+1]]
print("MUTANTX2", nQBI, sum(ACC), len(ACC), sum(ACC)/len(ACC), sum(T)/len(ACC))

frameworksData = {}
frameworksData["MutantX-S"] = {}
frameworksData["MutantX-S"]["Total Clone Search (s)"] = formatTime(sum(T))
frameworksData["MutantX-S"]["AVG Clone Search (s)"] = formatTimeAvg(sum(T)/len(T))	
frameworksData["MutantX-S"]["Precision"] = "{:.3f}".format(sum(ACC)/len(ACC))

df = pd.DataFrame(frameworksData).T
df.fillna(0, inplace=True)		
print(df)
