import numpy as np

from multiprocessing import Process
import time
import os



def run(O, nameXP):
    O0 = O[0]
    O1 = O[1]
    
    OALL = O0+O1
    
    for (idS,path,compilerOption,name, pathJson) in OALL:
        start = time.time()
        
        pathInput = "/".join(pathJson.split("/")[:-2]) + "/samples/"+str(idS)        
        pathOutput = "./CFG/"+nameXP[0:2]+"/" + str(idS)+".dot"
        command = "cfgbuilder "+pathInput+" > "+pathOutput
        
        os.system(command)
        elasped = time.time()-start
        print(nameXP[0:2],idS,elasped)

print("Can't be run because cfgbuilder is private property")

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CV 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_CO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UO 
    sys.path.insert(0, "????") # PSS_PATH_BASIC_UV 


    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    from makeBenchCV import benchmarkCV
    from makeBenchCO import benchmarkCO
    from makeBenchUO import benchmarkUO
    from makeBenchUV import benchmarkUV

    P1D = benchmarkBO("O0","O1")
    P6D = benchmarkBO("O2","O3")
    
    P7D = benchmarkBV("V0","V1")
    P12D = benchmarkBV("V2","V3")

    P13D = benchmarkCV("V0","V1")
    P18D = benchmarkCV("V2","V3")

    p1 = Process(target=run, args=(P1D,"BO0O1"))
    p1.start()

    p6 = Process(target=run, args=(P6D,"BO2O3"))
    p6.start()

    p7 = Process(target=run, args=(P7D,"BV0V1"))
    p7.start()

    p12 = Process(target=run, args=(P12D,"BV2V3"))
    p12.start()

    p1.join()
    p6.join()
    p7.join()     
    p12.join()    

    
    p13 = Process(target=run, args=(P13D,"CV0V1"))
    p13.start()

 
    p18 = Process(target=run, args=(P18D,"CV2V3"))
    p18.start()

    P1D = benchmarkCO("O0","O1")
    P6D = benchmarkCO("O2","O3")

    p1 = Process(target=run, args=(P1D,"CO0O1"))
    p1.start()
    
    p6 = Process(target=run, args=(P6D,"CO2O3"))
    p6.start()

    p1.join()
    p6.join()
    p13.join()    
    p18.join()
    

    P1D = benchmarkUO("O0","O1")
    P6D = benchmarkUO("O2","O3")
    P7D = benchmarkUV("V0","V1")
    P12D = benchmarkUV("V2","V3")


    p1 = Process(target=run, args=(P1D,"UO0O1"))
    p1.start()
  
    p6 = Process(target=run, args=(P6D,"UO2O3"))
    p6.start()

    p7 = Process(target=run, args=(P7D,"UV0V1"))
    p7.start()

    p12 = Process(target=run, args=(P12D,"UV2V3"))
    p12.start()

    p1.join()
    p6.join()
    p7.join()
    p12.join()
