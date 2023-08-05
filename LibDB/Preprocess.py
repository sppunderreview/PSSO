import numpy as np
import time
import re
import json

import pickle

from multiprocessing import Process
import subprocess


# https://github.com/1dayto0day/B2SFinder/blob/master/FeatureMatch/feature_match.py
def islist(value):
    return isinstance(value, list)

def is_web_name(line):
    p = re.compile('((https)?|ftp|file)(://)?(www.)[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    return (p.search(line))

def is_func_name(line):
    return bool(re.search('[a-z]', line)) & bool((re.search('[A-Z]', line)))

def has_special_char(line):
    return bool(re.search(r'\W', line, re.U)) | bool(re.search('_', line))

def hasNumbers(line):
    return bool(re.search(r'\d', line))

def get_word_key_value(word, program_name):
    weight = 0
    if word.isalpha():
        weight = 0.1
    if word.find(program_name) != -1:
        weight = weight + 5
    if word.islower():
        weight = weight + 0.1
    if word[1:].isupper():
        weight = weight + 0.25
    if hasNumbers(word):
        weight = weight + 0.25
    if has_special_char(word):
        weight = weight + 0.5
    if is_func_name(word[1:]):
        weight = weight + 0.5
    if is_web_name(word):
        weight = weight + 1
    return weight


def key_value(line, program_name):
    weight = 0
    if line.find(' ') != -1:
        for string in line.split(' '):
            weight = weight + get_word_key_value(string, program_name)
        weight = weight * (1 + len(line.split(' ')) * 0.1)
    else:
        weight = get_word_key_value(line, program_name)
    return weight


def computeEmbedding(inputs, nameXP):

    with open("GeminiEmbeds/"+nameXP+"_vecBYIdC", "rb") as f:
        geminiEmbeds = pickle.load(f)

    embeds = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:
        start = time.time()
        pathToSample = pathJson.split("/json")[0]+"/samples\\"+str(idS)


        with open(pathJson) as f:
            dataIDA = json.load(f)

        # exported function names ( https://stackoverflow.com/questions/12666253/elf-imports-and-exports )
        functionExportedNames = []
        P = subprocess.run(['readelf', "-sW", pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')
        lines = result.split("\n")
        for l in lines:
            if ("FUNC" in l) and (not("UND" in l )):
                functionExportedNames += [l.split(" ")[-2]]

        # call graph
        callGraph = {}
        idFToNameF = {}
        for f in dataIDA["functions"]:
            idFToNameF[f["id"]] =  f["name"]
            callGraph[f["name"]] = []

        for f in dataIDA["functions"]:
            for idNF in f["call"]:
                if idNF in idFToNameF:
                    callGraph[f["name"]] += [idFToNameF[idNF]]
                else:
                    callGraph[f["name"]] += [str(idNF)]

        # gemini embeddings
        geminiEmbedsS = {}
        for (nameF, v) in geminiEmbeds[idS]:
            if nameF in callGraph:
                geminiEmbedsS[nameF] = v

        # strings and weights
        strings = []

        # reading .rodata is enough for elf files
        P = subprocess.run(['readelf', "-x", ".rodata", pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')

        # Parse output
        hexdump = ""
        addressS = len("  0x0040c130 ")
        lines = result.split("\n")[2:-2]
        for l in lines:
            fL = l[addressS:]
            fL = fL.split("  ")[0]
            nFL = fL.split(" ")
            numberOfColumns = len(nFL)
            if numberOfColumns > 4:
                hexdump += "".join(nFL[:4])
            else:
                hexdump += "".join(nFL)

        hexdump  = hexdump.replace(" ", "")
        hexdump  = ' '.join(re.findall('..', hexdump))

        possibleFeatures = hexdump.split("00")[1:-1] # begin & end by \x00
        possibleFeatures = [ f.replace(" ", "") for f in possibleFeatures]

        for f in possibleFeatures:
            fB = bytes.fromhex(f)
            if len(fB) % 2 == 1:
                continue
            try:
                string  = fB.decode('utf-8')
                strings += [string]
            except UnicodeDecodeError:
                pass

        nDict = {}
        wDict = {}
        sumN = len(strings)

        for string in strings:
            wDict[string] = key_value(string, name)
            if not(string in nDict):
                nDict[string] = 0
            nDict[string] += 1

        elapsed = time.time() - start
        embeds[str(idS)] =  [set(functionExportedNames), callGraph, geminiEmbedsS, set(strings), wDict, nDict, sumN, elapsed]
        
        #print(compilerOption, name, elapsed)
        #print("F", len(functionExportedNames), len(callGraph))
        #print("EMBEDS", len(geminiEmbedsS), len(geminiEmbeds[idS]))
        #print("STRINGS", len(strings), "UNIQUE", len(wDict))
        #print()
    return embeds



def run(O, nameXP):
    embedsO = computeEmbedding(O, nameXP)    
    with open("A_"+nameXP, "wb") as f:
        pickle.dump(embedsO, f)
    
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    

    
    run(allBO(),"BO")
    run(allBV(),"BV")
    run(allUO(),"UO")
    run(allUV(),"UV")
    run(allCO(),"CO")
    run(allCV(),"CV")
