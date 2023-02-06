import sys

sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")

from makeBenchUO import benchmarkUO
from makeBenchUV import benchmarkUV

programFunctions = {}
O0, O1 = benchmarkUO("O0","O1")
O2, O3 = benchmarkUO("O2","O3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiUtilsOptions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]
        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("UO/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)

programFunctions = {}
O0, O1 = benchmarkUV("V0","V1")
O2, O3 = benchmarkUV("V2","V3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiUtilsVersions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]
        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("UV/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)

