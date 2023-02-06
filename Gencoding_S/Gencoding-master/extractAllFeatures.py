import os
import pickle


listProgram = [f for f in os.listdir("programsASM_G") if os.path.isfile(os.path.join("programsASM_G", f))]

for program in listProgram:	
	if program[-3:] != "elf":
		continue

	os.system("mv programsASM_G/"+program+" "+program)
	command = "ida64 -A -SextractFeatures.py "+program
	os.system(command)

	f = open("fileOut","r")
	cfgs = pickle.load(f)
	
	jsonFinal = ""

	for func in cfgs.raw_graph_list:
		functionName = func.funcname 
		edges = func.fun_features	
		attr = {}
		for node_id in func.old_g:
			attr[node_id] = func.retrieveVec(node_id, func.old_g)
			attr[node_id][0] = sum([ sum([ord(x) for x in s]) for s in attr[node_id][0] ])
			attr[node_id][1] = sum(attr[node_id][1])
		
		programSrc = program
		numBlocks = len(attr)
			
		
		succs = [[] for i in range(numBlocks)]
		for (u,v) in edges:
			if not(v in succs[u]):
				succs[u] += [v]
		
		features = []
		for i in range(numBlocks):
			features += [[float(x) % 10000 for x in attr[i]]]
		
		if numBlocks == 1:
			if features[0][-3] == 1.0:
				continue
		
		jsonFinal += "{\"src\": \""+programSrc+"\",";
		jsonFinal += "\"n_num\": "+str(numBlocks)+",";
		jsonFinal += "\"succs\": "+str(succs)+",";
		jsonFinal += "\"features\": "+str(features)+",";
		jsonFinal += "\"fname\": \""+functionName+"\"}\n";
	f.close()
	f = open("jsons/EGM_"+program+".json","w")
	f.write(jsonFinal)
	f.close()
	os.system("mv "+program+" programsASM_G/"+program)
	os.system("rm "+program+".*")

