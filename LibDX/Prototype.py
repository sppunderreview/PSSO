import numpy as np
import time
import subprocess

import re
import string

import pickle

import warnings

def computeEmbedding(inputs):
    printable_chars = set(bytes(string.printable, 'ascii'))

    embeds = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:        
        start = time.time()
        pathToSample = pathJson.split("/json")[0]+"/samples/"+str(idS)        
        
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

        # Select features
        possibleFeatures = hexdump.split("00")[1:-1] # begin & end by \x00
        possibleFeatures = [ f.replace(" ", "") for f in possibleFeatures]
        
        selectedFeatures = []        
        for f in possibleFeatures:
            # size > 5
            if len(f) <= 10:
                continue
            
            # all characters are printable
            fB = bytes.fromhex(f)
            if all(char in printable_chars for char in fB):
                selectedFeatures += [fB.decode('utf-8')]
            
        elapsed = time.time() - start
        print(compilerOption, name, len(selectedFeatures))
        embeds[str(idS)] =  [selectedFeatures,elapsed]        
    return embeds
    

def computeWeights(repository):
    embedsDS = {}
    for (DS, idS) in repository:
        if not(DS in embedsDS):
            with open("A_"+DS,"rb") as f:
                embedsDS[DS] = pickle.load(f)
        
    tokensInBinaries = {}    
    for (DS, idS) in repository:
        for tokenF in set(embedsDS[DS][str(idS)][0]):            
            if not(tokenF in tokensInBinaries):
                tokensInBinaries[tokenF] = []
            tokensInBinaries[tokenF] += [ (DS, idS) ]


    weights = {}
    weightPerBinary = {}
    
    for (DS, idS) in repository:
        if not(DS in weights):
            weights[DS] = {}
            weightPerBinary[DS] = {}
            
        weights[DS][idS] = {}
        weightPerBinary[DS][idS] = 0
        
        stringsOccs = {}
        for tokenF in embedsDS[DS][str(idS)][0]:
            if not(tokenF in stringsOccs):
                stringsOccs[tokenF] = 0
            stringsOccs[tokenF] += 1
        
        total = 0
        for s in stringsOccs:
            total += stringsOccs[s]
        
        for s in stringsOccs:
            tfidf = (stringsOccs[s] / total) * len(repository)
            tfidf /= len(tokensInBinaries[s])            
            weights[DS][idS][s] = tfidf
            weightPerBinary[DS][idS] += tfidf
    
    
    return weights, weightPerBinary
    

def computeMatchingMask(S):
    P_Flag = [ 0 for i in range(len(S))] 
    N_Flag = [ 0 for i in range(len(S))] 

    nP = 0
    nF = 0

    activePF = False
    activeNF = False

    startFP = 0
    startFN = 0

    anchorsP = []

    for i in range(len(S)):
        if S[i]:
            if nP == 0:
                startFP = i
            nP += 1
            nF  = 0

            if activeNF:
                for j in range(startFN, i):
                    N_Flag[j] = 1
            activeNF = False
                    
        else:
            if nF == 0:
                startFN = i    
            nF += 1       
            nP  = 0

            if activePF:
                for j in range(startFP, i):
                    P_Flag[j] = 1
                anchorsP += [startFP, i-1]
            activePF = False

        if nP == 10:
            activePF = True        

        if nF == 10:
            activeNF = True

    if activeNF:
        for j in range(startFN, len(S)):
            P_Flag[j] = 1
                    
    if activePF:
        for j in range(startFP, len(S)):
            N_Flag[j] = 1
        anchorsP += [startFP, i-1]
    
    logicMask = P_Flag

    for i in anchorsP:    
        for j in range(i,-1,-1):        
            if N_Flag[j]:
                break
            logicMask[j] = 1
            
        for j in range(i,len(logicMask)):        
            if N_Flag[j]:
                break
            logicMask[j] = 1
    return logicMask

def distanceLibDX(DS, idS, DS2, idS2, embeds, W):    
    featuresidS = set( embeds[DS][str(idS)][0] )
        
    # Compute matching fragments
    S = []
    for s in embeds[DS2][str(idS2)][0]:
        S += [ int( s in featuresidS  )]
    logicMask = computeMatchingMask(S)
    
    # Apply logic blocks mask
    for i in range(len(S)):
        S[i] *= logicMask[i]
    
    # Retrieve string matched
    stringMatched = {}    
    for i in range(len(S)):
        if S[i]:
            stringMatched[ embeds[DS2][str(idS2)][0][i] ] = True
    
    
    # Compute matching ratio
    (w, weightPerBinary) = W
    
    ratio = 0    
    for s in stringMatched:
        ratio += w[DS2][idS2][s]
    if weightPerBinary[DS2][idS2]  == 0:
        warnings.warn(str((DS2, idS2,  embeds[DS2][str(idS2)][0])))
        return 100
        
    ratio /= weightPerBinary[DS2][idS2]
    return 1 - ratio
