# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")

from correctBenchBO import readToCorrect

import pickle
import json

from utils.function_normalizer import FunctionNormalizer
from utils.instructions_converter import InstructionsConverter
from utils.capstone_disassembler import disassemble
from safetorch.safe_network import SAFE
from safetorch.parameters import Config
import torch


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

asm = ""
arch = "x86"
bits = 64

for (idS, path, compilerOption, name, pathJson) in readToCorrect():
    with open(pathJson) as f:
        data = json.load(f)
      
    idProgram = str(idS)
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
     
    pathOutput = "BOC\\"+idProgram
    
    with open(pathOutput, "wb") as f:
        pickle.dump(functionsData,f)
