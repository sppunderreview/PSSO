from multiprocessing import Process
import pickle

import os

def run(O, nameXP):
    P = 40
    numberPrograms = len(O)
    outputFile = nameXP+"_MD"
    
    distancesFinal = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    for idCore in range(P):
        with open(nameXP+"/results_"+str(idCore), 'rb') as f:
            distances = pickle.load(f)
            for i in range(numberPrograms):
                for j in range(numberPrograms):
                    if distances[i][j] != 0:
                        distancesFinal[i][j] = distances[i][j]
    t = 0
    for idCore in range(P):        
        if nameXP == "BO" and os.path.isfile(nameXP+"C/results_"+str(idCore)):
            with open(nameXP+"C/results_"+str(idCore), 'rb') as f:
                distances = pickle.load(f)
                for i in range(numberPrograms):
                    for j in range(numberPrograms):
                        if distances[i][j] != 0:
                            distancesFinal[i][j] = distances[i][j]
                            t += 1
    print(nameXP, "TOTAL", t)
            
    elapsedFinal = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    for idCore in range(P):
        with open(nameXP+"/elapsed_"+str(idCore), 'rb') as f:
            elapsed = pickle.load(f)
            for i in range(numberPrograms):
                for j in range(numberPrograms):
                    if elapsed[i][j] != 0:
                        elapsedFinal[i][j] = elapsed[i][j]
    for idCore in range(P):
        if nameXP == "BO" and os.path.isfile(nameXP+"C/elapsed_"+str(idCore)):
            with open(nameXP+"C/elapsed_"+str(idCore), 'rb') as f:
                elapsed = pickle.load(f)
                for i in range(numberPrograms):
                    for j in range(numberPrograms):
                        if elapsed[i][j] != 0:
                            elapsedFinal[i][j] = elapsed[i][j]

    MD = {}
    for (idS,path,compilerOption,name, pathJson) in O:
        MD[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2:
                continue
            d = distancesFinal[idS][idS2]
            elpased = elapsedFinal[idS][idS2]
            MD[idS][idS2] = (name,name2,compilerOption,compilerOption2,d,elpased)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)                

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    
    p1 = Process(target=run, args=(allBO(),"BO"))
    p1.start()

    p2 = Process(target=run, args=(allBV(),"BV"))
    p2.start()
   
    p3 = Process(target=run, args=(allUO(),"UO"))
    p3.start()
    p4 = Process(target=run, args=(allUV(),"UV"))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
   

    p5 = Process(target=run, args=(allCV(),"CV"))
    p5.start()
    p6 = Process(target=run, args=(allCO(),"CO"))
    p6.start()
    
    p5.join()
    p6.join()
    

