import numpy as np
import time
import subprocess
import pickle

from tqdm import tqdm

def computeEmbeddings(inputs):
    embedsB = 0
    embeds = {}
	
    for (idS, pathToSample) in tqdm(inputs):        
        start = time.time()
        P = subprocess.run(['strings', pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')
		
        stringMultiSet = {}
        for s in result.split("\n"):
            t = s.replace("\r","")
            if not(t in stringMultiSet):
                stringMultiSet[t] = 0
            stringMultiSet[t] += 1
        
        elapsed = time.time() - start
        embeds[str(idS)] = [stringMultiSet, elapsed]
        
        if len(embeds) == 100:
            with open("Features/B_"+str(embedsB), "wb") as f:
                pickle.dump(embeds, f)
            embeds = {}
            embedsB += 1   
    
    # Last block
    with open("Features/B_"+str(embedsB), "wb") as f:
        pickle.dump(embeds, f)
