import pickle

toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3"),("O0","O1"),("O0","O2"),("O0","O3"),("O1","O2"),("O1","O3"),("O2","O3")]

for DS in ["C","B","U"]:
    for O0, O1 in toDo:        
        folder = "ASM_"+DS+O0[0]+ "_gDist/"+DS+O0+O1+"/"        
        with open(folder+"elapsed_0", 'rb') as f:
            elapsed = pickle.load(f)
        
        numberPrograms = len(elapsed)
        elapsedFinal = [[0 for i in range(numberPrograms)] for j in range(numberPrograms)]
        
        for idCore in range(40):
            with open(folder+"elapsed_"+str(idCore), 'rb') as f:
                elapsed = pickle.load(f)
                for i in range(numberPrograms):
                    for j in range(numberPrograms):
                        if elapsed[i][j] != 0:
                            elapsedFinal[i][j] = elapsed[i][j]
        with open(folder+"elapsed", 'wb') as f:
            pickle.dump(elapsedFinal, f)
        
