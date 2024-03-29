import pickle
import numpy as np
import sys
import random

import time

def computesDistance(E1,E2):
    
    start = time.time()
    intersectionExtern = E1[1].intersection(E2[1])    
    
    embedsF1 = []
    for f in range(len(E1[0])): 
        embedsF1+= [(E1[0][f][0],E1[0][f][1],np.array([int(extern in E1[0][f][2]) for extern in intersectionExtern]))]        
    
    embedsF2 = []
    for f in range(len(E2[0])): 
        embedsF2+= [(E2[0][f][0],E2[0][f][1],np.array([int(extern in E2[0][f][2]) for extern in intersectionExtern]))]        
        
    dTotal = 0
    for (X0,X1,X2) in embedsF1:        
        dMin = None
        for (Y0,Y1,Y2) in embedsF2:
            d = np.linalg.norm(X0-Y0) + np.linalg.norm(X2-Y2) -(0.75**np.linalg.norm(X1-Y1))
            if dMin == None or d < dMin:
                dMin = d        
        dTotal += dMin
    et = time.time() - start
    return dTotal, et

def main():
    args = sys.argv[1:]
    myId = int(args[0])
    maxID = int(args[1])
    maxIDO = 35
    myIdO = 33

    targets = ["recutils-1.7_gcc-6.4.0_x86_32_O2_librec.so.1.0.0.elf","coreutils-8.29_gcc-6.4.0_x86_32_O2_libstdbuf.so.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgsl.so.23.1.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libiconv.so.2.6.0.elf","libtasn1-4.13_gcc-6.4.0_x86_32_O2_libtasn1.so.6.5.5.elf","libmicrohttpd-0.9.59_gcc-6.4.0_x86_32_O2_libmicrohttpd.so.12.46.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libhistory.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosip2.so.12.0.0.elf","lightning-2.1.2_gcc-6.4.0_x86_32_O2_liblightning.so.1.0.0.elf","libunistring-0.9.10_gcc-6.4.0_x86_32_O2_libunistring.so.2.1.0.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgslcblas.so.0.0.0.elf","libtool-2.4.6_gcc-6.4.0_x86_32_O2_libltdl.so.7.3.1.elf","gmp-6.1.2_gcc-6.4.0_x86_32_O2_libgmp.so.10.3.2.elf","gdbm-1.15_gcc-6.4.0_x86_32_O2_libgdbm.so.6.0.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libreadline.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosipparser2.so.12.0.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libcharset.so.1.0.0.elf","gsasl-1.8.0_gcc-6.4.0_x86_32_O2_libgsasl.so.7.9.6.elf","gss-1.0.3_gcc-6.4.0_x86_32_O2_libgss.so.3.0.3.elf","glpk-4.65_gcc-6.4.0_x86_32_O2_libglpk.so.40.3.0.elf"]
    with open("vecById", 'rb') as f:
        vecById = pickle.load(f)

    random.seed(10)
    distances = {}
    elapsed =   {}
    for j in targets:
        distances[j] = {}
        elapsed[j]   = {}
        for i in vecById:
            distances[j][i] = 0
            elapsed[j][i]   = 0

    tasks = []
    for t in targets:
        for p in vecById:
            if p == t:
                continue
            tasks += [(t,p)]
    random.shuffle(tasks)
    # Get the 33/35 original part
    batchSize = int((1/maxIDO) * len(tasks)) + 1
    startT = batchSize * myIdO
    endT   = batchSize * (myIdO+1)
    taskS = tasks[startT:endT]

    # Split by ID
    batchSize = int((1/maxID) * len(taskS)) + 1
    startT = batchSize * myId
    if myId == maxID - 1:
        endT = len(taskS)
    else:
        endT = batchSize * (myId+1)
    taskS2 = taskS[startT:endT]
    print(len(taskS2))

    for (t,p) in taskS2:
        d, et = computesDistance(vecById[t],vecById[p])
        distances[t][p] = d
        elapsed[t][p] = et

    with open("MD/results2_"+str(myId), 'wb') as f:
        pickle.dump(distances, f)
    with open("MD/elapsed2_"+str(myId), 'wb') as f:
        pickle.dump(elapsed, f)

if __name__ == "__main__":
    main()
