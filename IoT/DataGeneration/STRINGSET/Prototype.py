import numpy as np
import time
import subprocess
import pickle

def computeEmbedding(inputs):
    embeds = {}
    for idS in inputs:
        start = time.time()
        pathToSample = "../DATA/samples/"+idS
        P = subprocess.run(['strings', pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')
		
        stringMultiSet = {}
        for s in result.split("\n"):
            t = s.replace("\r","")
            if not(t in stringMultiSet):
                stringMultiSet[t] = 0
            stringMultiSet[t] += 1             
        elapsed = time.time() - start
        embeds[str(idS)] =  stringMultiSet # [stringMultiSet, time.time() - start]
    return embeds
    
