from Prototype import computeClosests
import pickle

def run(O, nameDS):
    outputFile = nameDS+"_MD"

    # Create repository for weights
    R   = []
    for (idS,path,compilerOption,name, pathJson) in O:
        R    += [(nameDS, idS)]

    closestD = computeClosests(R, R)

    MD = {}
    for (idS,path,compilerOption,name, pathJson) in O:
        MD[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O:
            if idS == idS2:
                continue
            if closestD[nameDS][idS][1] == idS2:
                d = 0
            else:
                d = 1
            MD[idS][idS2] = (name,name2,compilerOption,compilerOption2,d, closestD[nameDS][idS][2])

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 


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

