import time
import json
import pickle

from os.path import isfile
from pathlib import Path
import numpy as np

# {4-gram -> freq}
def hashEmbedding(D):
	embed = [0 for i in range(4096)]	
	for ngram in D:
		t = ngram.replace("??", "ff")
		t = t.replace("-", "f")
		
		isBinary = True
		for c in t:
			if not(c in ["0","1", " "]):
				isBinary = False
				break
		t = t.split("_")
		t = [x for x in t if x != "" ]
		
		if isBinary:
			ngramInt = [ int(s, 2) for s in t]
		else:
			ngramInt = [ int(s, 16) for s in t]
		hashNgram = 7		
		for x in ngramInt:
			hashNgram = 31 * hashNgram + x
		p = hashNgram % 4096

		embed[p] += D[ngram]	
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

# https://wiki.osdev.org/X86-64_Instruction_Encoding
# http://ref.x86asm.net/

prefixX32 = {}
for p in ["66","f2","f3","2e","9b","64","65","f0","36","3e","26"]:
	prefixX32[p] = True

def findOpcodeX32(instrBytes):
	global prefixX32
	# x32 prefix
	while(len(instrBytes) > 1 and (instrBytes[0:2] in prefixX32)):
		instrBytes = instrBytes[2:]
	
	if len(instrBytes) < 2:
		return "??"
	
	# REX x32 prefix
	if (instrBytes[0] == "4"):
		if (len(instrBytes) < 4):
			return "??"
		instrBytes = instrBytes[2:]

	# Opcode	
	# 2 bytes
	if (len(instrBytes) >= 4 and instrBytes[0:2] == "0f"):		   
		return instrBytes[0:4]
	# 1 byte
	return instrBytes[0:2]


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

def condReverse(instrBytes, endian):
	if endian != "le":
		return instrBytes
	instrBytes2 = ""
	for i in range(len(instrBytes)-1, 0, -2):
			instrBytes2 += instrBytes[i-1]+instrBytes[i]
	return instrBytes2

def findOpcodeArm(instrBytes, endian):	
	instrBytes = condReverse(instrBytes, endian)
	return bin(int(instrBytes, 16))[3+2:7+2]

def findOpcodeMips(instrBytes, endian):
	instrBytes = condReverse(instrBytes, endian)
	return bin(int(instrBytes, 16))[0+2:6+2]

def findOpcodeSparc(instrBytes, endian):
	instrBytes = condReverse(instrBytes, endian)
	mainOp = bin(int(instrBytes, 16))[0+2:2+2]
	if mainOp == "01":
		return mainOp
	if mainOp == "00":
		return bin(int(instrBytes, 16))[7+2:10+2]
	return bin(int(instrBytes, 16))[7+2:13+2]

def findOpcode68040(instrBytes):
	return instrBytes[0:2]
	
def findOpcode390(instrBytes):
	return bin(int(instrBytes, 16))[0+2:8+2]	

	
		
def computesEmbeddingFromBytes(idS, pathInput):	
	opcodesTotal  = []
	with open(pathInput) as f:
		data = json.load(f)
	
	endianess = data["architecture"]["endian"]
	
	if data["architecture"]["type"] in ["arm","armb"]:
		start = time.time()
		for instrBytes in data["bytes"]:
			opcodesTotal += [findOpcodeArm(instrBytes, endianess)]
	elif data["architecture"]["type"] in ["mips","sh4","ppc","sh3","sh4b","ppcl"] :
		start = time.time()
		for instrBytes in data["bytes"]:
			opcodesTotal += [findOpcodeMips(instrBytes, endianess)]
	elif data["architecture"]["type"] in ["sparcb","arcmpct","arcv2"] :
		start = time.time()
		for instrBytes in data["bytes"]:
			opcodesTotal += [findOpcodeSparc(instrBytes, endianess)]
	elif data["architecture"]["type"] in ["68040"] :
		start = time.time()
		for instrBytes in data["bytes"]:
			opcodesTotal += [findOpcode68040(instrBytes)]
	elif data["architecture"]["type"] in ["s390x"] :
		start = time.time()
		for instrBytes in data["bytes"]:
			opcodesTotal += [findOpcode390(instrBytes)]
	else:
		if data["architecture"]["type"] != "metapc":
			print(idS, "error not metapc",data["architecture"]["type"])
			return
		
		
		size = int(data["architecture"]["size"][1:3])
		if not(size in [32, 64]):
			print(idS, "error not 32/64",data["architecture"]["size"])
			return
		start = time.time()
		
		if (size == 32):
			for instrBytes in data["bytes"]:
				opcodesTotal += [findOpcodeX32(instrBytes)]
		else:	
			for instrBytes in data["bytes"]:
				opcodesTotal += [findOpcodeX64(instrBytes)]

	embedding = computeEmbedding(opcodesTotal)
	elasped = time.time()-start
	#print(idS, data["architecture"], elasped, len(opcodesTotal))
	return embedding

TODO = []
for path in Path('../bytes/').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1]
	idS = idS.replace("_bytes", "")
	TODO += [(pathString, idS)]		
	

E = {}

u = 0
start = time.time()
for (pathInput, idS)  in TODO:
	try:
		E[idS] = computesEmbeddingFromBytes(idS, pathInput)
	except Exception as e:
		print("Exception:",idS,e)
	u += 1
	if u % 100 == 0:			
		timeLeft = ((len(TODO) - u)) * ((time.time()-start)/u)
		print(u*100/len(TODO),"%",int(timeLeft), "s")


with open("MUTANTX2", "wb") as f:
	pickle.dump(E,f)
