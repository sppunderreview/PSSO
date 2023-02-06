from multiprocessing import Process
import pickle

def run(O, nameXP):
    inputFile =  nameXP[0:2]+"_MD"
    with open(inputFile, 'rb') as f:
        MD3 = pickle.load(f)
    
    outputFile = nameXP+"_MD"
    
    O0 = O[0]
    O1 = O[1]
                        
    MD = {}
    MD["->"] = {}
    MD["<-"] = {}
    MD["<>"] = {}


    for (idS,path,compilerOption, name, pathJson) in O0:
        MD["->"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O1:
            d = MD3[idS][idS2][-2]
            MD["->"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)
            

    for (idS,path,compilerOption,name, pathJson) in O1:
        MD["<-"][idS] = {}        
        for (idS2,path2,compilerOption2,name2, pathJson2) in O0:
            d = MD3[idS][idS2][-2]
            MD["<-"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

    OAll = O0 + O1

    for (idS,path,compilerOption,name, pathJson) in OAll:
        MD["<>"][idS] = {}        
        for (idS2,path2,compilerOption2,name2, pathJson2) in OAll:
            if idS == idS2:
                continue
            d = MD3[idS][idS2][-2]
            MD["<>"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)
        
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")

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

    p1 = Process(target=run, args=(P1D,"BO0O1"))
    p1.start()

    p2 = Process(target=run, args=(P2D,"BO0O2"))
    p2.start()

    p3 = Process(target=run, args=(P3D,"BO0O3"))
    p3.start()

    p4 = Process(target=run, args=(P4D,"BO1O2"))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    p5 = Process(target=run, args=(P5D,"BO1O3"))
    p5.start()

    p6 = Process(target=run, args=(P6D,"BO2O3"))
    p6.start()

    p7 = Process(target=run, args=(P7D,"BV0V1"))
    p7.start()

    p8 = Process(target=run, args=(P8D,"BV0V2"))
    p8.start()

    p5.join()
    p6.join()
    p7.join()
    p8.join()
    
    p9 = Process(target=run, args=(P9D,"BV0V3"))
    p9.start()

    p10 = Process(target=run, args=(P10D,"BV1V2"))
    p10.start()

    p11 = Process(target=run, args=(P11D,"BV1V3"))
    p11.start()

    p12 = Process(target=run, args=(P12D,"BV2V3"))
    p12.start()

    p9.join()
    p10.join()
    p11.join()
    p12.join()
    
    p13 = Process(target=run, args=(P13D,"CV0V1"))
    p13.start()

    p14 = Process(target=run, args=(P14D,"CV0V2"))
    p14.start()

    p15 = Process(target=run, args=(P15D,"CV0V3"))
    p15.start()

    p16 = Process(target=run, args=(P16D,"CV1V2"))
    p16.start()

    p13.join()
    p14.join()
    p15.join()
    p16.join()
    
    p17 = Process(target=run, args=(P17D,"CV1V3"))
    p17.start()

    p18 = Process(target=run, args=(P18D,"CV2V3"))
    p18.start()

    p17.join()
    p18.join()

    P1D = benchmarkCO("O0","O1")
    P2D = benchmarkCO("O0","O2")
    P3D = benchmarkCO("O0","O3")
    P4D = benchmarkCO("O1","O2")
    P5D = benchmarkCO("O1","O3")
    P6D = benchmarkCO("O2","O3")

    p1 = Process(target=run, args=(P1D,"CO0O1"))
    p1.start()

    p2 = Process(target=run, args=(P2D,"CO0O2"))
    p2.start()

    p3 = Process(target=run, args=(P3D,"CO0O3"))
    p3.start()

    p4 = Process(target=run, args=(P4D,"CO1O2"))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    p5 = Process(target=run, args=(P5D,"CO1O3"))
    p5.start()

    p6 = Process(target=run, args=(P6D,"CO2O3"))
    p6.start()

    p5.join()
    p6.join()

    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")

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


    p1 = Process(target=run, args=(P1D,"UO0O1"))
    p1.start()

    p2 = Process(target=run, args=(P2D,"UO0O2"))
    p2.start()

    p3 = Process(target=run, args=(P3D,"UO0O3"))
    p3.start()

    p4 = Process(target=run, args=(P4D,"UO1O2"))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    p5 = Process(target=run, args=(P5D,"UO1O3"))
    p5.start()

    p6 = Process(target=run, args=(P6D,"UO2O3"))
    p6.start()

    p7 = Process(target=run, args=(P7D,"UV0V1"))
    p7.start()

    p8 = Process(target=run, args=(P8D,"UV0V2"))
    p8.start()

    p5.join()
    p6.join()
    p7.join()
    p8.join()
    
    p9 = Process(target=run, args=(P9D,"UV0V3"))
    p9.start()

    p10 = Process(target=run, args=(P10D,"UV1V2"))
    p10.start()

    p11 = Process(target=run, args=(P11D,"UV1V3"))
    p11.start()

    p12 = Process(target=run, args=(P12D,"UV2V3"))
    p12.start()

    p9.join()
    p10.join()
    p11.join()
    p12.join()
    