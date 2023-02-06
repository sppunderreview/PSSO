from multiprocessing import Process
import pickle
import os

def run(O, nameXP):
    numberPrograms = len(O)
    outputFile = nameXP+"_MD"
    
    distancesFinal = [[1 for i in range(numberPrograms)] for j in range(numberPrograms)]
    elapsedFinal = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
    
    listFiles = []
    for root, dirs, files in os.walk(nameXP):
        for file in files:
            if file.endswith(".txt"):
                 listFiles += [os.path.join(root, file)]
    
    for logFile in listFiles:
        with open(logFile, "r") as f:
            lines = f.readlines()
            
            for l in lines:
                t = l[1:-2].replace(",","").split(" ")            
                idS = int(t[1])
                idS2 = int(t[2])
                d = float(t[3])
                elapsed = float(t[4])
                
                if idS in [5,6,12]: # Corrected
                    continue
                distancesFinal[idS][idS2] = d
                elapsedFinal[idS][idS2] = elapsed
    
    if nameXP == "BO":
        for p in range(40):
            nameFile = "BOC/BOC_"+str(p)+"_log.txt"
            if os.path.isfile(nameFile) == False:
                continue
            with open(nameFile, "r") as f:
                lines = f.readlines()            
                for l in lines:
                    t = l[1:-2].replace(",","").split(" ")            
                    idS = int(t[1])
                    idS2 = int(t[2])
                    d = float(t[3])
                    elapsed = float(t[4])
                    distancesFinal[idS][idS2] = d
                    elapsedFinal[idS][idS2] = elapsed
    
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
    

