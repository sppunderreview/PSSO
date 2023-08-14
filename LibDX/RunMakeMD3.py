from Prototype import computeWeights, distanceLibDX

from multiprocessing import Process
import pickle
import time

def minRun(O, embeds, outputFile, nameDS):
    embedsMultiDS = {}
    embedsMultiDS[nameDS] = embeds
    
    # Create repository for weights
    R   = []
    for (idS,path,compilerOption,name, pathJson) in O:
        R    += [(nameDS, idS)]
        
    # Computes weights
    W    = computeWeights(R)

    MD = {}
    for (idS,path,compilerOption,name, pathJson) in O:
        MD[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2:
                continue
            start = time.time()
            d = distanceLibDX(nameDS, idS, nameDS, idS2, embedsMultiDS, W)
            elpased = time.time()-start
            MD[idS][idS2] = (name,name2,compilerOption,compilerOption2,d, elpased)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)

def run(O, nameDS):
    with open("A_"+nameDS, "rb") as f:
        embeds = pickle.load(f)

    minRun(O, embeds, nameDS+"_MD", nameDS)

print("This is not used in the paper, since it handle repository containing all programs of a subdataset.")
print("Need 30 minutes.")


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    
    run(allBO(),"BO")
    run(allBV(),"BV")
    run(allUO(),"UO")
    run(allUV(),"UV")
    run(allCV(),"CV")
    run(allCO(),"CO")
