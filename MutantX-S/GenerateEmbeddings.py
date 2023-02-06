import time
import json
import pickle

from multiprocessing import Process

import numpy as np

def hashEmbedding(d):
	embed = [0 for i in range(4096)]
	
	for ngram in d:
		t = ngram.replace("??", "ff")
		t = t.split("_")
		ngramInt = [ int(s, 16) for s in t]
		hashNgram = 7		
		for x in ngramInt:
			hashNgram = 31 * hashNgram + x
		p = hashNgram % 4096
		embed[p] += d[ngram]		
	return np.array(embed)
    
# 4 grams embedding
def computeEmbedding(opcodes):
    ngrams = zip(*[opcodes[i:] for i in range(4)])    
    embedding = {}
    for ngram in ngrams:
        d = "_".join(ngram)
        if not(d in embedding):
            embedding[d] = 0        
        embedding[d] += 1
    
    return hashEmbedding(embedding)

prefixX64 = {}
for p in ["f0","f2","f3","2f","36","3f","26","64","65","2e","3e","66","67"]:
    prefixX64[p] = True
    
def findOpcodeX64(instrBytes):
    global prefixX64
    # x64 prefix
    while(len(instrBytes) > 1 and (instrBytes[0:2] in prefixX64)):
        instrBytes = instrBytes[2:]
    
    if len(instrBytes) < 2:
        return "??"
    
    # REX x64 prefix
    if (instrBytes[0] == "4"):
        if (len(instrBytes) < 4):
            return "??"
        instrBytes = instrBytes[2:]

    # Opcode    
    # 2 bytes
    if (len(instrBytes) >= 4 and instrBytes[0:2] == "0f"):
        # 3 bytes
        if (len(instrBytes) >= 6 and instrBytes[2:4] in ["38","3a"]):
            return instrBytes[0:6]             
        return instrBytes[0:4]
    # 1 byte
    return instrBytes[0:2]

def computesEmbeddingFromBytes(nameDS, idS):
    pathInput = "./bytes/"+nameDS+"/bytes_" + str(idS)+".json"
    pathOutput = "./A/"+nameDS+"/"+str(idS)
    
    opcodesTotal  = []
    with open(pathInput) as f:
        data = json.load(f)
    
    if data["architecture"]["type"] != "metapc":
        print(nameDS, idS, "error not metapc",data["architecture"]["type"])
        return
    
    
    size = int(data["architecture"]["size"][1:3])
    if not(size in [64]):
        print(nameDS, idS, "error not 32/64",data["architecture"]["size"])
        return
    
    start = time.time()
    
    for instrBytes in data["bytes"]:
        opcodesTotal += [findOpcodeX64(instrBytes)]

    embedding = computeEmbedding(opcodesTotal)
    elasped = time.time()-start
    print(idS,elasped, len(opcodesTotal), len(embedding))
    data = (embedding,elasped)
    with open(pathOutput, "wb") as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    PN = 4

    toDo = [("UO",88),("UV",88),("BO",84),("BV",84),("CO", 416),("CV", 348)]
    
    for (nameDS, maxIDS) in toDo:
        dataToDo = [idS for idS in range(maxIDS)]    
        while len(dataToDo) > 0:
            i = 0
            P = []
            for idS in dataToDo:
                p = Process(target=computesEmbeddingFromBytes, args=(nameDS,idS))
                p.start()
                P += [p]
                i += 1
                if i == PN:
                    break
            for p in P:
                p.join()
            dataToDo = dataToDo[PN:]

    
