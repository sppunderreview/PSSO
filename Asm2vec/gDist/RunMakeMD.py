import sys
sys.path.insert(0, "C:\\Users\\?\\Desktop\GUtilsOptions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\GUtilsVersions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\GCoreutilsOptions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\GCoreutilsVersions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\GBigOptions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\GBigVersions")

from makeBenchCO import benchmarkCO
from makeBenchCV import benchmarkCV
from makeBenchUO import benchmarkUO
from makeBenchUV import benchmarkUV
from makeBenchBO import benchmarkBO
from makeBenchBV import benchmarkBV

import pickle

def run(O, nameXP):
    O0 = O[0]
    O1 = O[1]
    
    inputMatrix = "ASM_"+nameXP[0:2]+"_gDist/"+nameXP+"/results"
    outputFile = "../"+nameXP+"_MD"

    with open(inputMatrix, "rb") as f:
        distances = pickle.load(f)
            
    MD = {}
    MD["->"] = {}
    MD["<-"] = {}
    MD["<>"] = {}
    
    for (idS,path,compilerOption,name, pathJson) in O0:
        MD["->"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O1:
            d =  distances[idS][idS2]
            MD["->"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)
            
    for (idS,path,compilerOption,name, pathJson) in O1:
        MD["<-"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O0:
            d =  distances[idS][idS2]
            MD["<-"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

        
    OTotal = O0+O1

    for (idS,path,compilerOption,name, pathJson) in OTotal:
        MD["<>"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in OTotal:
            if idS == idS2:
                continue
            d =  distances[idS][idS2]
            MD["<>"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)


run(benchmarkCO("O0","O1"),"CO0O1")
run(benchmarkCO("O0","O2"),"CO0O2")
run(benchmarkCO("O0","O3"),"CO0O3")
run(benchmarkCO("O1","O2"),"CO1O2")
run(benchmarkCO("O1","O3"),"CO1O3")
run(benchmarkCO("O2","O3"),"CO2O3")

run(benchmarkCV("V0","V1"),"CV0V1")
run(benchmarkCV("V0","V2"),"CV0V2")
run(benchmarkCV("V0","V3"),"CV0V3")
run(benchmarkCV("V1","V2"),"CV1V2")
run(benchmarkCV("V1","V3"),"CV1V3")
run(benchmarkCV("V2","V3"),"CV2V3")

run(benchmarkUO("O0","O1"),"UO0O1")
run(benchmarkUO("O0","O2"),"UO0O2")
run(benchmarkUO("O0","O3"),"UO0O3")
run(benchmarkUO("O1","O2"),"UO1O2")
run(benchmarkUO("O1","O3"),"UO1O3")
run(benchmarkUO("O2","O3"),"UO2O3")

run(benchmarkUV("V0","V1"),"UV0V1")
run(benchmarkUV("V0","V2"),"UV0V2")
run(benchmarkUV("V0","V3"),"UV0V3")
run(benchmarkUV("V1","V2"),"UV1V2")
run(benchmarkUV("V1","V3"),"UV1V3")
run(benchmarkUV("V2","V3"),"UV2V3")

run(benchmarkBO("O0","O1"),"BO0O1")
run(benchmarkBO("O0","O2"),"BO0O2")
run(benchmarkBO("O0","O3"),"BO0O3")
run(benchmarkBO("O1","O2"),"BO1O2")
run(benchmarkBO("O1","O3"),"BO1O3")
run(benchmarkBO("O2","O3"),"BO2O3")

run(benchmarkBV("V0","V1"),"BV0V1")
run(benchmarkBV("V0","V2"),"BV0V2")
run(benchmarkBV("V0","V3"),"BV0V3")
run(benchmarkBV("V1","V2"),"BV1V2")
run(benchmarkBV("V1","V3"),"BV1V3")
run(benchmarkBV("V2","V3"),"BV2V3")