import pickle
from tqdm import tqdm

def minRun(O, folder, nameXP):
    inputFile  = folder+nameXP[0:2]+"_MD"
    with open(inputFile, 'rb') as f:
        MD3 = pickle.load(f)
                        
    outputFile = folder+nameXP+"_MD"
    
    O0 = O[0]
    O1 = O[1]
            
    MD = {}
    MD["->"] = {}
    MD["<-"] = {}
    MD["<>"] = {}

    print("Testfield", O0[0][2], "->", O1[0][2])
    for (idS,path,compilerOption, name, pathJson) in tqdm(O0):
        MD["->"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in  O1:
            d = MD3[idS][idS2][-2]
            MD["->"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)
            
    print("Testfield", O0[0][2], "<-", O1[0][2])
    for (idS,path,compilerOption,name, pathJson) in tqdm(O1):
        MD["<-"][idS] = {}        
        for (idS2,path2,compilerOption2,name2, pathJson2) in O0:
            d = MD3[idS][idS2][-2]
            MD["<-"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

    OAll = O0 + O1

    print("Testfield", O0[0][2], "<->", O1[0][2])
    for (idS,path,compilerOption,name, pathJson) in tqdm(OAll):
        MD["<>"][idS] = {}        
        for (idS2,path2,compilerOption2,name2, pathJson2) in OAll:
            if idS == idS2:
                continue
            d = MD3[idS][idS2][-2]
            MD["<>"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)

def run(O, nameXP):
    print("Basic Subdataset", nameXP[0:2])
    minRun(O, "./", nameXP)
    #minRun(O, "../spectralA/",  nameXP)
    #minRun(O, "../spectralB/",  nameXP)
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 

    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    from makeBenchCV import benchmarkCV
    from makeBenchCO import benchmarkCO

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

    P13D = benchmarkCV("V0","V1")
    P14D = benchmarkCV("V0","V2")
    P15D = benchmarkCV("V0","V3")
    P16D = benchmarkCV("V1","V2")
    P17D = benchmarkCV("V1","V3")
    P18D = benchmarkCV("V2","V3")

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
    
    run(P13D,"CV0V1")
    run(P14D,"CV0V2")
    run(P15D,"CV0V3")
    run(P16D,"CV1V2")
    run(P17D,"CV1V3")
    run(P18D,"CV2V3")
    
    P1D = benchmarkCO("O0","O1")
    P2D = benchmarkCO("O0","O2")
    P3D = benchmarkCO("O0","O3")
    P4D = benchmarkCO("O1","O2")
    P5D = benchmarkCO("O1","O3")
    P6D = benchmarkCO("O2","O3")

    run(P1D,"CO0O1")
    run(P2D,"CO0O2")
    run(P3D,"CO0O3")
    run(P4D,"CO1O2") 
    run(P5D,"CO1O3")
    run(P6D,"CO2O3")
    
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 

    from makeBenchUO import benchmarkUO
    from makeBenchUV import benchmarkUV

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
    
