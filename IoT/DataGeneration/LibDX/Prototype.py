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
    for idS in inputs:        
        start = time.time()
        pathToSample = "../DATA/samples/"+idS
        
        P = subprocess.run(['readelf', "-x", ".rodata", pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')
        
        # Remove messages
        lines = result.split("\n")
        linesS = []
        for l in lines:
            if len(l) < 5 or (not("  0x" in l) ):
                continue
            linesS += [l]
        
        # Handle empty section
        if len(linesS) == 0:
            embeds[str(idS)] =  [] #[[],time.time()-start]
            continue
                
        # Parse output
        lines = linesS
        hexdump = ""
        addressS = len("  0x0040c130 ")
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
        possibleFeatures = hexdump.split("00")[1:-1] # begin and end by \x00
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
            
        embeds[str(idS)] =  selectedFeatures # [selectedFeatures, time.time() - start]        
    return embeds
