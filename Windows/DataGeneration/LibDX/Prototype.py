import numpy as np
import time

import pefile
import re
import string

import pickle

def computeEmbedding(inputs):
    printable_chars = set(bytes(string.printable, 'ascii'))

    idF = 0
    featuresID = {}
    embeds = {}

    for (idS, pathToSample) in inputs:        
        start = time.time()

        # Get hexdump of .rdata
        hexdump = b""     
        
        # Handle exceptions
        try:
            pe = pefile.PE(pathToSample)
            for section in pe.sections:
                if not(".rdata" in str(section.Name.decode('utf-8'))):
                    continue
                hexdump = section.get_data()
                break
        except Exception as e:
            print(idS, e)
				
        # Handle exceptions / no .rdata section
        if len(hexdump) == 0:
            print(idS, "no valid .rdata")
            embeds[str(idS)] =  [[], time.time() - start]
            continue

        hexdump  = hexdump.hex(' ')

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
		
		# Optimize memory
        selectedFeaturesEncoded = []
        for f in selectedFeatures:
            if not(f in featuresID):
                featuresID[f] = idF
                idF += 1
            selectedFeaturesEncoded += [featuresID[f]]
            
        embeds[str(idS)] =  [selectedFeaturesEncoded, time.time() - start]
    return embeds, featuresID
