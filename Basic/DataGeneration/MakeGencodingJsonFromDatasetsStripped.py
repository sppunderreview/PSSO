# Need to be run with the .sh file

from os import system

print "Hello, here is the script to replay the disassembly with IDA and features extraction with Gencoding.\n"
print "It extract from samples from each Basic Dataset to get Gemini features.\n"


print "Enter the absolute path to IDApro v7.5 folder:"
pathIdaFolder = raw_input()
# /home/tristan/idapro-7.5/

# Put IDA into python2 mode
system("touch "+pathIdaFolder+"/python/use_python2")


nameFolders = [("CoreutilsVersions","CV"), ("CoreutilsOptions","CO"), ("UtilsVersions", "UV"), ("UtilsOptions", "UO"), ("BigVersions", "BV"), ("BigOptions","BO")]
for (nameFolder, _) in nameFolders:
	pathSamples = "./Datasets/"+nameFolder+"/samples/"
	
	# Perform copies
	system("mkdir ./Gencoding_Stripped/programs")
	system("cp "+pathSamples+"* ./Gencoding_Stripped/programs")

	# Run Gencoding script
	system("cd ./Gencoding_Stripped && python extractAllFeatures.py")

	# Move the ouput
	system("mv ./Gencoding_Stripped/extractedGeminiStripped.json ./extractedGeminiStripped"+nameFolder+".json")
	print "Gencoding extraction performed!"

	# Remove copies
	system("rm -r ./Gencoding_Stripped/programs")


# Recover IDA into python3 mode
system("rm  "+pathIdaFolder+"/python/use_python2")
