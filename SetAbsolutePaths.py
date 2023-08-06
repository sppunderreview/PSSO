import os

CONST_PATH_REVERSED = {"PSS_PATH_BASIC_BO" : "BigOptions", "PSS_PATH_BASIC_BV" : "BigVersions", "PSS_PATH_BASIC_CV" : "CoreutilsVersions", "PSS_PATH_BASIC_CO" : "CoreutilsOptions", "PSS_PATH_BASIC_UV" : "UtilsVersions", "PSS_PATH_BASIC_UO" : "UtilsOptions"}

# Detect files
filesInsidePSSO = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] in [".py"]]
filesDetectedPythonIncludeBasic = {}
for path in filesInsidePSSO:
	with open(path, "r") as f:
		i = 0
		for l in f.readlines():
			i += 1
			if "sys.path.insert" in l:
				filesDetectedPythonIncludeBasic[path] = True
				break

#print(len(filesDetectedPythonIncludeBasic))
#print(filesDetectedPythonIncludeBasic)

# Ask user
print("Enter the absolute path to 'PSSO/Basic' folder:")
pathBasic = input() # /home/tristan/Documents/Travail/TransfertGit/PSSO/Basic

# Set absolute paths using tags
for path in filesDetectedPythonIncludeBasic:
	nL = []
	with open(path, "r") as f:
		for l in f.readlines():
			t = l
			if "sys.path.insert" in t:
				idCONST = None
				for trigger in CONST_PATH_REVERSED:
					if trigger in t:
						idCONST = trigger
						break				
				if idCONST == None:
					nL += [t]
					continue
				absolutePath = os.path.join(pathBasic,"G"+CONST_PATH_REVERSED[idCONST])				
				newT = t.split("\"")[0]+"\""+absolutePath+"\") # "+idCONST+" \n"
				nL += [newT]
			else:
				nL += [t]

	T = "".join(nL)
	with open(path, "w") as f2:
		f2.write(T)

