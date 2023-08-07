from os import system

print("Hello, here is the script to replay the disassembly of Basic datasets with IDA.\n")

print("Enter the absolute path to IDApro v7.5 folder:") 
pathIdaFolder = input()
print("Enter the absolute path to the 'ExtractBinaryIDA.py' script inside 'JsonExtractor' folder:") 
pathScript = input()

system("rm "+pathIdaFolder+"/python/use_python2")


nameFolders = [("CoreutilsVersions","CV"), ("CoreutilsOptions","CO"), ("UtilsVersions", "UV"), ("UtilsOptions", "UO"), ("BigVersions", "BV"), ("BigOptions","BO")]

for (nameFolder, initial) in nameFolders:
	print("Basic dataset:", nameFolder)
	pathSamples = "./Datasets/"+nameFolder+"/samples/"
	
	# Run Ida script
	command = "java -jar -Xmx6g JsonExtractor.jar "+pathSamples+" "+pathIdaFolder+" "+pathScript
	system(command)
	
	# Put json files into a folder
	pathJson = 	"./Datasets/"+nameFolder+"/jsons/"
	system("mkdir "+pathJson)		
	system("mv "+pathSamples+"*.json* "+pathJson)
	system("rm "+pathSamples+"*.*")

	# Give a unique name to the file listing the empty functions
	system("mv "+pathSamples+"../functionsToRemove.txt "+pathSamples+"../functionsToRemove_"+initial+".txt")

	print("Basic dataset", nameFolder, "DONE")
	print("Files generated into folder:", "./Datasets/"+nameFolder)
