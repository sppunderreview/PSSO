import os
import pickle
from multiprocessing import Process

def run(O, nameXP):
    O0 = O[0]
    O1 = O[1]
    
    outputFile = "../"+nameXP[0:2]+"_MD"
    if os.path.exists(outputFile) == False:
        MD3 = {}
    else:
        with open(outputFile, "rb") as f:
            MD3 = pickle.load(f)
            
    inputFile = "../"+nameXP+"_MD"    
    with open(inputFile, "rb") as f:
        MD = pickle.load(f)
        
    inputElpased = "ASM_"+nameXP[0:2]+ "_gDist/"+nameXP+"/elapsed"   
    with open(inputElpased, "rb") as f:
        Elapsed = pickle.load(f)
        
    OTotal = O0+O1
    for (idS,path,compilerOption,name, pathJson) in OTotal:
        if not(idS in MD3):
            MD3[idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in OTotal:
            if idS == idS2:
                continue
            _, _, _ ,_ , d = MD["<>"][idS][idS2] 
            t = Elapsed[idS][idS2]                
            MD3[idS][idS2]  = (name,name2,compilerOption,compilerOption2,d,t)
        
    with open(outputFile, "wb") as f:
        pickle.dump(MD3, f)

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 
    

    
    from makeBenchCO import benchmarkCO
    from makeBenchCV import benchmarkCV
    from makeBenchUO import benchmarkUO
    from makeBenchUV import benchmarkUV
    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    
    P1D = benchmarkCO("O0","O1")
    P2D = benchmarkCO("O0","O2")
    P3D = benchmarkCO("O0","O3")
    P4D = benchmarkCO("O1","O2")
    P5D = benchmarkCO("O1","O3")
    P6D = benchmarkCO("O2","O3")

    P7D = benchmarkCV("V0","V1")
    P8D = benchmarkCV("V0","V2")
    P9D = benchmarkCV("V0","V3")
    P10D = benchmarkCV("V1","V2")
    P11D = benchmarkCV("V1","V3")
    P12D = benchmarkCV("V2","V3")


    run(P1D,"CO0O1")
    run(P2D,"CO0O2")
    run(P3D,"CO0O3")
    run(P4D,"CO1O2")
    run(P5D,"CO1O3")
    run(P6D,"CO2O3")
    
    run(P7D,"CV0V1")
    run(P8D,"CV0V2")
    run(P9D,"CV0V3")
    run(P10D,"CV1V2")
    run(P11D,"CV1V3")
    run(P12D,"CV2V3")


    P1D = benchmarkUO("O0","O1")
    P2D = benchmarkUO("O0","O2")
    P3D = benchmarkUO("O0","O3")
    P4D = benchmarkUO("O1","O2")
    P5D = benchmarkUO("O1","O3")
    P6D = benchmarkUO("O2","O3")

    P7D = benchmarkUV("V0","V1")
    P8D = benchmarkUV("V0","V2")
    P9D = benchmarkUV("V0","V3")
    P10D = benchmarkUV("V1","V2")
    P11D = benchmarkUV("V1","V3")
    P12D = benchmarkUV("V2","V3")


    run(P1D,"UO0O1")
    run(P2D,"UO0O2")
    run(P3D,"UO0O3")
    run(P4D,"UO1O2")
    run(P5D,"UO1O3")
    run(P6D,"UO2O3")
    
    run(P7D,"UV0V1")
    run(P8D,"UV0V2")
    run(P9D,"UV0V3")
    run(P10D,"UV1V2")
    run(P11D,"UV1V3")
    run(P12D,"UV2V3")

    P1D = benchmarkBO("O0","O1")
    P2D = benchmarkBO("O0","O2")
    P3D = benchmarkBO("O0","O3")
    P4D = benchmarkBO("O1","O2")
    P5D = benchmarkBO("O1","O3")
    P6D = benchmarkBO("O2","O3")

    P7D = benchmarkBV("V0","V1")
    P8D = benchmarkBV("V0","V2")
    P9D = benchmarkBV("V0","V3")
    P10D = benchmarkBV("V1","V2")
    P11D = benchmarkBV("V1","V3")
    P12D = benchmarkBV("V2","V3")


    run(P1D,"BO0O1")
    run(P2D,"BO0O2")
    run(P3D,"BO0O3")
    run(P4D,"BO1O2")
    run(P5D,"BO1O3")
    run(P6D,"BO2O3")
    
    run(P7D,"BV0V1")
    run(P8D,"BV0V2")
    run(P9D,"BV0V3")
    run(P10D,"BV1V2")
    run(P11D,"BV1V3")
    run(P12D,"BV2V3")
