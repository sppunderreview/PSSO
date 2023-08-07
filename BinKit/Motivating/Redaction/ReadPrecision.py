from pathlib import Path
import pickle

import numpy as np

def readMD(pathD):
	L = []
	for path in Path(pathD+"/MD/").rglob('r*'):
		L += [str(path)]	
	MD = {}	
	for path in L:
		with open(path, "rb") as f:
			MDP = pickle.load(f)		
		for idS in MDP:
			if not(idS in MD):
				MD[idS] = {}
			for idS2 in MDP[idS]:
				if MDP[idS][idS2]!= 0:
					MD[idS][idS2] = [MDP[idS][idS2],0]
	L = []
	for path in Path(pathD+"/MD/").rglob('e*'):
		L += [str(path)]	
	for path in L:
		with open(path, "rb") as f:
			EP = pickle.load(f)
		for idS in EP:
			for idS2 in EP[idS]:
				if not(idS2 in MD[idS]):
					MD[idS][idS2] = [0,0]
				if EP[idS][idS2] != 0:
					MD[idS][idS2][1] = EP[idS][idS2]
	return MD

def readLIBDB(R):
	path = "../LibDB/MO_"+R+"_MD"
	with open(path, "rb") as f:
		MD = pickle.load(f)	
	MD2 = {}	
	for idS in MD["->"]:
		MD2[idS] = {}
		for idS2 in MD["->"][idS]:
			MD2[idS][idS2] = [MD["->"][idS][idS2][-2],MD["->"][idS][idS2][-1]]
	return MD2

def pokeContent(MD, T):
	for idS in T:
		for idS2 in MD[idS]:
			if idS == idS2:
				continue
			print(idS,idS2,MD[idS][idS2])
			break
		break

def score(MD, T, R):
	ACC = []
	for idS in T:
		idSelected = ""
		minD = None
		for idS2 in R:
			if idS == idS2:
				continue			
			d = MD[idS][idS2][0]
			if minD == None or d < minD:
				minD = d
				idSelected = idS2
		n  = "_".join(idS.split("_")[5:])
		n2 = "_".join(idSelected.split("_")[5:])
		ACC += [n == n2]
	return sum(ACC)/len(ACC)

def distancePSS(A,B):
    k  = min(len(A[0]),len(B[0]))
    k2 = min(len(A[1]),len(B[1]))
    return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def scorePSS(E, T, R):
	ACC = []
	for idS in T:
		idSelected = ""
		minD = None
		for idS2 in R:
			if idS == idS2:
				continue			
			d = distancePSS(E[idS],E[idS2])
			if minD == None or d < minD:
				minD = d
				idSelected = idS2
		n  = "_".join(idS.split("_")[5:])
		n2 = "_".join(idSelected.split("_")[5:])
		ACC += [n == n2]
	return sum(ACC)/len(ACC)

T = ["recutils-1.7_gcc-6.4.0_x86_32_O2_librec.so.1.0.0.elf","coreutils-8.29_gcc-6.4.0_x86_32_O2_libstdbuf.so.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgsl.so.23.1.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libiconv.so.2.6.0.elf","libtasn1-4.13_gcc-6.4.0_x86_32_O2_libtasn1.so.6.5.5.elf","libmicrohttpd-0.9.59_gcc-6.4.0_x86_32_O2_libmicrohttpd.so.12.46.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libhistory.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosip2.so.12.0.0.elf","lightning-2.1.2_gcc-6.4.0_x86_32_O2_liblightning.so.1.0.0.elf","libunistring-0.9.10_gcc-6.4.0_x86_32_O2_libunistring.so.2.1.0.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgslcblas.so.0.0.0.elf","libtool-2.4.6_gcc-6.4.0_x86_32_O2_libltdl.so.7.3.1.elf","gmp-6.1.2_gcc-6.4.0_x86_32_O2_libgmp.so.10.3.2.elf","gdbm-1.15_gcc-6.4.0_x86_32_O2_libgdbm.so.6.0.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libreadline.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosipparser2.so.12.0.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libcharset.so.1.0.0.elf","gsasl-1.8.0_gcc-6.4.0_x86_32_O2_libgsasl.so.7.9.6.elf","gss-1.0.3_gcc-6.4.0_x86_32_O2_libgss.so.3.0.3.elf","glpk-4.65_gcc-6.4.0_x86_32_O2_libglpk.so.40.3.0.elf"]

AD = readMD("../AlphaDiff/AD_MO_gDist")
Asm2Vec = readMD("../Asm2Vec/gDist")
Gemini = readMD("../Gemini/Gemini_MO_gDist")
Safe = readMD("../SAFE/SAFE_MO_gDist")

R32 = []
R64 = []
RALL = []
RO0 = []
RO1 = []
RO2 = []
RO3 = []
RCLANG = []
RGCC   = []

# ['recutils-1.7', 'clang-5.0', 'x86', '32', 'O1', 'librec.so.1.0.0.elf']
for idS in AD["recutils-1.7_gcc-6.4.0_x86_32_O2_librec.so.1.0.0.elf"]:
	t = idS.split("_")
	b = t[3]
	c = t[4]
	n = "_".join(t[5:])
	if b == "32":
		R32 += [idS]
	elif b == "64":
		R64 += [idS]

	if c == "O0":
		RO0 += [idS]
	elif c == "O1":
		RO1 += [idS]
	elif c == "O2":
		RO2 += [idS]
	elif c == "O3":
		RO3 += [idS]

	if "clang" in idS:
		RCLANG += [idS]
	elif "gcc" in idS:
		RGCC += [idS]
	RALL += [idS]

EMB = [AD,Asm2Vec,Gemini,Safe]
RS = [RO0,RO1,RO2,RO3,RCLANG,RGCC,R32,R64,RALL]

print([len(x) for x in RS])

for MD in EMB:
	for R in RS:
		print(score(MD,T,R))
	print()
	print()

R_LIBDB = [("O0",RO0),("O1",RO1),("O2",RO2),("O3",RO3),("CLANG",RCLANG),("GCC",RGCC),("32",R32),("64",R64),("ALL",RALL)]
for (r,R) in R_LIBDB:
	MD = readLIBDB(r)
	print(score(MD,T,R))
print()
print()

with open("PSS", "rb") as f:
	PSS = pickle.load(f)

for (r,R) in R_LIBDB:
	print(scorePSS(PSS,T,R))
print()
print()

