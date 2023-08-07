import numpy as np
import time

import subprocess
import re
import string

import pickle

from tqdm import tqdm

def computeEmbedding(inputs):
	printable_chars = set(bytes(string.printable, 'ascii'))

	idF = 0
	featuresID = {}
	embeds = {}

	for (idS, pathToSample) in tqdm(inputs):		
		start = time.time()
		
		selectedFeatures = []

		# Handle exceptions
		try:
			P = subprocess.run(['readelf', "-x", ".rodata", pathToSample], stdout=subprocess.PIPE)
			result = P.stdout.decode('utf-8')			
			# Parse output
			hexdump = ""
			lines = result.split("\n")[2:-2]
			for l in lines:
				fL = l.split(" ")
				fL = fL[3:7]
				hexdump += "".join(fL)
			hexdump  = hexdump.replace(" ", "")
			hexdump  = ' '.join(re.findall('..', hexdump))
			
			# Select features
			possibleFeatures = hexdump.split("00")[1:-1] # begin & end by \x00
			possibleFeatures = [ f.replace(" ", "") for f in possibleFeatures]
			
			for f in possibleFeatures:
				# size > 5
				if len(f) <= 10:
					continue
				
				# all characters are printable
				fB = bytes.fromhex(f)
				if all(char in printable_chars for char in fB):
					selectedFeatures += [fB.decode('utf-8')]
		except Exception as e:
			print(idS, e)
		
		# Optimize memory
		selectedFeaturesEncoded = []
		for f in selectedFeatures:
			if not(f in featuresID):
				featuresID[f] = idF
				idF += 1
			selectedFeaturesEncoded += [featuresID[f]]
		 
		embeds[str(idS)] =  [selectedFeaturesEncoded, time.time() - start]
	return embeds, featuresID
