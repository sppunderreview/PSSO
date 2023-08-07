# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import pickle
import json

from utils.function_normalizer import FunctionNormalizer
from utils.instructions_converter import InstructionsConverter
from utils.capstone_disassembler import disassemble
from safetorch.safe_network import SAFE
from safetorch.parameters import Config
import torch

import time
from pathlib import Path
from os import system
from os.path import isfile, join, getsize

from random import shuffle
from multiprocessing import Process

def computeEmbeds(goodware, myId, maxId):
	# initialize SAFE
	config = Config()
	safe = SAFE(config)

	# load instruction converter and normalizer
	I2V_FILENAME = "model/word2id.json"
	converter = InstructionsConverter(I2V_FILENAME)
	normalizer = FunctionNormalizer(max_instruction=150)

	# load SAFE weights
	SAFE_torch_model_path = "model/SAFEtorch.pt"
	state_dict = torch.load(SAFE_torch_model_path)
	safe.load_state_dict(state_dict)
	safe = safe.eval()
	
	# parallelize data
	L = []
	i = 0
	for pathString in goodware:
		if i % maxId == myId:
			L += [pathString]
		i += 1
		
	start = time.time()
	j = 0
	for (idProgram, arch, bits, pathJson) in L:
		with open(pathJson, "r")  as f:
			data = json.load(f)
		functionsData = {}
		for f in data["functions"]:
			idFunction = "P_"+idProgram+"F_"+str(f["id"])
			
			nameF = f["name"]
			
			asm = ""
			for b in f["blocks"]:
				if "bytes" in b:
					asm += b["bytes"]
			
			
			instructions = disassemble(asm, arch, bits)
			converted_instructions = converter.convert_to_ids(instructions)
			functions, length = normalizer.normalize_functions([converted_instructions])
			tensor = torch.LongTensor(functions[0])
			function_embedding = safe(tensor, length).detach().numpy()
			functionsData[idFunction] = (nameF, function_embedding)
			
		pathOutput = "EMBEDS/"+idProgram
		with open(pathOutput, "wb") as f:
			pickle.dump(functionsData,f)

		j += 1		
		if j % 10 == 0:
			timePerElement = (time.time()-start)/j
			print(myId, int((len(L)-j)*timePerElement), "s")

PN = 3

# collect files
goodware = []
for path in Path('../../jsons').rglob('*'):
	pathString = str(path)
	if not(isfile(pathString)):
		continue
	idS = pathString.split("/")[-1].replace(".tmp.json", "")
	t = idS.split("_")	
	arch = t[2]
	bits = int(t[3])

	if arch != "x86":
		continue
		
	if isfile("EMBEDS/"+idS):
		continue
	goodware += [(idS, arch, bits, pathString)]

shuffle(goodware)
print(len(goodware))

P = []
for i in range(PN):
	p = Process(target=computeEmbeds, args=(goodware,i, PN))
	p.start()
	P += [p]
for p in P:
	p.join()


    
