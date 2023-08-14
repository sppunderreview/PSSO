import time
import os
from multiprocessing import Process

print("Need 4 hours divided by the number of cores")

def extractBytesFromProgram(nameDS, idS, subPath):	
    pathIntput = os.path.join("/".join(os.path.abspath(__file__).split("/")[:-2]), "Basic", "G"+subPath, "samples", str(idS) )
    pathIdaOut = pathIntput+"_bytes.json"    
    pathOutput = "./bytes/"+nameDS+"/bytes_" + str(idS)+".json"    
    pathScript = os.path.join("/".join(os.path.abspath(__file__).split("/")[:-1]), "ExtractBytesViaIDA.py")
    command = "idat64"+ " -A -S"+pathScript+" "+pathIntput
    commandCopy = "cp "+pathIdaOut+" "+pathOutput

    os.system(command)
    os.system(commandCopy)
    

if __name__ == '__main__':
    PN = 36

    toDo = [("UO",88,"UtilsOptions"),("UV",88,"UtilsVersions"),("BO",84,"BigOptions"),("BV",84,"BigVersions"),("CO", 416, "CoreutilsOptions"),("CV", 348, "CoreutilsVersions")]
    
    for (nameDS, maxIDS, subPath) in toDo:
        dataToDo = [idS for idS in range(maxIDS)]    
        while len(dataToDo) > 0:
            i = 0
            P = []
            for idS in dataToDo:
                p = Process(target=extractBytesFromProgram, args=(nameDS,idS, subPath))
                p.start()
                P += [p]
                i += 1
                if i == PN:
                    break
            for p in P:
                p.join()
            dataToDo = dataToDo[PN:]

    
