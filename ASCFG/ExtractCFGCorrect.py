import numpy as np

from multiprocessing import Process
import time
import os

print("Can't be run because cfgbuilder is private property")
print("Old correction that is useless to replicate now")

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    from correctBenchBO import readToCorrect

    for (idS,path,compilerOption,name, pathJson) in readToCorrect():
        start = time.time()
        
        pathInput = "/".join(pathJson.split("/")[:-2]) + "/samples/"+str(idS)        
        pathOutput = "./CFG/"+nameXP[0:2]+"/" + str(idS)+".dot"
        command = "cfgbuilder "+pathInput+" > "+pathOutput
        
        os.system(command)
        elasped = time.time()-start
        print(nameXP[0:2],idS,elasped)



