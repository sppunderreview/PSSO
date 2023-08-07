import pickle

with open("familiesMetaElf", "rb") as f:
	hashToFamilies = pickle.load(f)

familiesByPriority = ['pnscan', 'vpnfilter', 'hajime', 'lightaidra', 'dnsamp', 'skeeyah', 'ddostf', 'tsunami', 'gafgyt', 'mirai']
labelsAssigned = {}

Labels = {}

IoT = []
for hashS in hashToFamilies:
	idS = hashS+".elf"
	hashS = idS.replace(".elf","")
	trueLabel = len(familiesByPriority) - 1
	for i in range(len(familiesByPriority)):		
		if familiesByPriority[i] in hashToFamilies[hashS]:
			trueLabel = i
			break
	
	textLabel = familiesByPriority[trueLabel]
	if not(textLabel in labelsAssigned):
		labelsAssigned[textLabel] = 0
	labelsAssigned[textLabel] += 1	
	
	if trueLabel in [7,8,9]:
		Labels[idS] = trueLabel - 7

print(labelsAssigned)

with open("LABELS_P", "wb") as f:
	pickle.dump(Labels, f)
