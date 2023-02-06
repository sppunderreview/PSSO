from os import system
import sys
import random

sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")


from makeBenchBO import benchmarkBO
from makeBenchBV import benchmarkBV
from makeBenchCV import benchmarkCV
from makeBenchCO import benchmarkCO

programFunctions = {}
O0, O1 = benchmarkBO("O0","O1")
O2, O3 = benchmarkBO("O2","O3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiBigOptions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]
        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("BO/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)

programFunctions = {}
O0, O1 = benchmarkBV("V0","V1")
O2, O3 = benchmarkBV("V2","V3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiBigVersions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]
        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("BV/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)

programFunctions = {}
O0, O1 = benchmarkCO("O0","O1")
O2, O3 = benchmarkCO("O2","O3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiCoreutilsOptions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]

        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("CO/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)
            
programFunctions = {}
O0, O1 = benchmarkCV("V0","V1")
O2, O3 = benchmarkCV("V2","V3")
ALL = O0+O1+O2+O3

namePrograms = {}
for (idS,path,compilerOption,name, pathJson) in ALL:
    namePrograms[str(idS)] = name

with open("extractedGeminiCoreutilsVersions.json", "r") as f:
    for l in f.readlines():
        p = l.split(",")[0].split("\"")[-2]
        if not(p in programFunctions):
            programFunctions[p] = []
        programFunctions[p] += [l]

for p in programFunctions:
    with open("CV/"+p+".json", "w") as f:
        for l in programFunctions[p]:
            l = l.replace("\"fname\": \"","\"fname\": \""+namePrograms[p]+"_")
            f.write(l)