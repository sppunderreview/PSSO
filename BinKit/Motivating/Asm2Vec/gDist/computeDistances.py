import pickle
import numpy as np
import sys
import random
import time

def computesDistance(vectorsP1,vectorsP2):
    start = time.time()
    dL = 0
    for v in vectorsP1:
        dLM = 1000
        for v2 in vectorsP2:
            d =  np.linalg.norm(v2-v, ord=2)
            if d < dLM:
                dLM = d
        dL += dLM
    et = time.time() - start
    return dL, et

def main():
    args = sys.argv[1:]
    myId = int(args[0])
    maxID = int(args[1])
    
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
        #print(len(vecById[t]))
        for p in vecById:
            if p == t:
                continue
            tasks += [(t,p)]

    random.shuffle(tasks)
    batchSize = int((1/maxID) * len(tasks)) + 1

    startT = batchSize * myId
    if myId == maxID - 1:
        endT = len(tasks)
    else:
        endT = batchSize * (myId+1)

    for i in range(startT, endT):
        t = tasks[i][0]
        p = tasks[i][1]
        d, et = computesDistance(vecById[t],vecById[p])
        distances[t][p] = d
        elapsed[t][p] = et

    with open("MD/results_"+str(myId), 'wb') as f:
        pickle.dump(distances, f)
    with open("MD/elapsed_"+str(myId), 'wb') as f:
        pickle.dump(elapsed, f)

if __name__ == "__main__":
    main()
