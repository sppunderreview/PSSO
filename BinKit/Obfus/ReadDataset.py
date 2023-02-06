import pickle 

def reverseDict(dict):
    rd = {}    
    for charact in dict:        
        for idS in dict[charact]:
            rd[idS] = charact
    return rd
    
def addToDict(dict, charact, idS):
    if not(charact in dict):
        dict[charact] = []
    dict[charact] += [idS]
    
def listCharacs(dict):
    print([(x,len(dict[x])) for x in dict])

def collectQB(dict):
    QBs = []
    for x in dict:
        for y in dict:
            if x == y:
                continue
            n = x+"/"+y
            if not("normal" in n):
                continue          
            print(n)    
            QBs += [[n, dict[x], dict[y]]]
    return QBs

with open("NORMAL_EMBEDS_2/BSIZE", "rb") as f:
    IDS_NORMAL = set([idS for idS in pickle.load(f)])

with open("OBFUS_EMBEDS/BSIZE", "rb") as f:
    IDS_OBF = set([idS for idS in pickle.load(f)])

"""
EMBEDS = ["BSIZE","DSIZE","FUNCTIONSET","LIBDX","MUTANTX2","PSS","PSSV16","SCG","SHAPE","STRINGS"]
for n in EMBEDS:
    with open(n, "rb") as f:
        O = set([idS for idS in pickle.load(f)])
        IDS = IDS.intersection(O)
"""

NNames = {}
for idS in IDS_NORMAL:
    t = idS.split("_")
    project   = t[0]
    #compiler  = t[1]
    #arch      = t[2]
    #endianess = t[3]
    #optim     = t[4] 
    nameProgram = project+"_"+"_".join(t[5:])
    addToDict(NNames, nameProgram, idS)

Obfs = {}
ONames = {}
for idS in IDS_OBF:
    t = idS.split("_")
    project   = t[0]
    compiler  = t[1]
    #arch      = t[2]
    #endianess = t[3]
    #optim     = t[4] 
    nameProgram = project+"_"+"_".join(t[5:])
    addToDict(Obfs, compiler, idS)
    addToDict(ONames, nameProgram, idS)

T = reverseDict(NNames)
T.update(reverseDict(ONames))
print(len(T)) # 105 280
with open("T", "wb") as f:
    pickle.dump(T, f)

Obfus = {}
Obfus['normal']   =   [y for x in NNames for y in NNames[x]]
for x in Obfs:
    Obfus[x]   =   [y for y in Obfs[x]]

listCharacs(Obfus)
# [('normal', 67680), ('clang-obfus-bcf', 9400), ('clang-obfus-fla', 9400), ('clang-obfus-sub', 9400), ('clang-obfus-all', 9400)]

QBs = collectQB(Obfus)
with open("QBs", "wb") as f:
    pickle.dump(QBs, f)