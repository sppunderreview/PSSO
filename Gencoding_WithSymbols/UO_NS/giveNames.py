#!/usr/bin/python3

# ? ?
# 2021
# ?

from os import system

dataset = "uo"

with open("samples.txt", "r") as f:
	nbP = int(f.readline().strip())
	for i in range(nbP):
		idS = int(f.readline().strip())		
		path = f.readline().strip()
		name = path.split("/")[-1]		
		pathSample = "samples/"+str(idS)
		dest = "samplesN/"+dataset+"_"+name+"_"+str(idS)
		command = "cp "+pathSample+" "+dest
		print(command)
		system(command)
