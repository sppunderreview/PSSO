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
	tableIdPath[idSample] = pathString
	pathsExist[pathString] = True
	idSample +=  1

with open("samples.txt", "w") as f:
	f.write(str(len(tableIdPath))+"\n")
	for idS in tableIdPath:
		f.write(str(idS)+"\n")
		f.write(str(tableIdPath[idS])+"\n")
		command = "cp \'"+tableIdPath[idS]+ "\' ./samples/"+str(idS)
		print(command)
		system(command)

