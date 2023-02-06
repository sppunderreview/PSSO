#!/usr/bin/python3

# ? ?
# 2021
# ?

from os import system, remove
from os.path import isfile, join, getsize
from pathlib import Path

idSample = 0
tableIdPath = {}
pathsExist = {}

for path in Path('binaries').rglob('*'):
	if isfile(path) == False:
		continue
	pathString = str(path)
	name = pathString.split("/")[-1]
	tableIdPath[idSample] = pathString
	pathsExist[pathString] = True
	idSample +=  1


programTaken = {}
for idS in tableIdPath:
	name = tableIdPath[idS].split("/")[-1]
	if name in programTaken:
		continue
	if  ("binaries/coreutils-8.30-O0/"+name in pathsExist) and ("binaries/coreutils-8.30-O1/"+name in pathsExist) and ("binaries/coreutils-8.30-O2/"+name in pathsExist) and ("binaries/coreutils-8.30-O3/"+name  in pathsExist) :
		programTaken[name] = True

idS2 = 0
finaltableIdPath = {}

for idS in tableIdPath:
	name = tableIdPath[idS].split("/")[-1]
	if name in programTaken:
		finaltableIdPath[idS2] = tableIdPath[idS]
		idS2 += 1

print(len(programTaken))
print(len(finaltableIdPath))

with open("samples.txt", "w") as f:
	f.write(str(len(finaltableIdPath))+"\n")
	for idS in finaltableIdPath:
		f.write(str(idS)+"\n")
		f.write(str(finaltableIdPath[idS])+"\n")
		command = "cp \'"+finaltableIdPath[idS]+ "\' ./samples/"+str(idS)
		print(command)
		system(command)

