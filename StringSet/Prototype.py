import numpy as np
import time
import subprocess

def computeEmbedding(inputs):
    embeds = {}
    for (idS,path,compilerOption,name, pathJson) in inputs:        
        start = time.time()
        pathToSample = pathJson.split("\\json")[0]+"\\samples\\"+str(idS)        
        P = subprocess.run(['strings.exe', pathToSample], stdout=subprocess.PIPE)
        result = P.stdout.decode('utf-8')
        stringMultiSet = {}
        for s in result.split("\n"):
            t = s.replace("\r","")
            if not(t in stringMultiSet):
                stringMultiSet[t] = 0
            stringMultiSet[t] += 1             
        elapsed = time.time() - start        
        embeds[str(idS)] =  [stringMultiSet,elapsed]        
    return embeds