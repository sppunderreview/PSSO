import time
from os import system
from multiprocessing import Process


def extractBytesFromProgram(nameDS, idS, subPath):
    pathIntput = "/home/?/Documents/Travail/?/"+subPath+"/samples/"+str(idS) 
    pathIdaOut = pathIntput+"_bytes.json"    
    pathOutput = "./"+nameDS+"/bytes_" + str(idS)+".json"
    
    command = "/home/?/idapro-7.5/idat64 -A -S/home/?/Documents/Travail/?/MutantX/ExtractBytesViaIDA.py "+pathIntput
    commandCopy = "cp "+pathIdaOut+" "+pathOutput

    system(command)
    system(commandCopy)
    

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

    
