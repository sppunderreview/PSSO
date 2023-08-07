from Prototype import computeClosests

from multiprocessing import Process
import pickle
import time

def run(O, nameXP):
    print(nameXP)
    start = time.time()
    nameDS = "MO"
    outputFile = "MO_"+nameXP+"_MD"

    O0 = O[0]
    O1 = O[1]

    # Create repository
    R_O0   = []
    R_O1   = []
    for (idS,path,compilerOption,name, pathJson) in O0:
        R_O0    += [(nameDS, idS)]
    for (idS,path,compilerOption,name, pathJson) in O1:
        R_O1    += [(nameDS, idS)]

    MD = {}
    MD["->"] = {}
    MD_LIBDB    = computeClosests(R_O0, R_O1)

    for (idS,path,compilerOption, name, pathJson) in O0:
        MD["->"][idS] = {}
        for (idS2,path2,compilerOption2,name2, pathJson2) in O1:
            if idS2 in MD_LIBDB[nameDS][idS][nameDS]:
                d = -MD_LIBDB[nameDS][idS][nameDS][idS2][0]
                el = MD_LIBDB[nameDS][idS][nameDS][idS2][1]
                MD["->"][idS][idS2] = (name,name2,compilerOption,compilerOption2,d, el)
            else:
                MD["->"][idS][idS2] = (name,name2,compilerOption,compilerOption2,1, 0)

    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)

    print(nameXP, time.time()-start)

if __name__ == '__main__':
    targets = set(["recutils-1.7_gcc-6.4.0_x86_32_O2_librec.so.1.0.0.elf","coreutils-8.29_gcc-6.4.0_x86_32_O2_libstdbuf.so.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgsl.so.23.1.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libiconv.so.2.6.0.elf","libtasn1-4.13_gcc-6.4.0_x86_32_O2_libtasn1.so.6.5.5.elf","libmicrohttpd-0.9.59_gcc-6.4.0_x86_32_O2_libmicrohttpd.so.12.46.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libhistory.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosip2.so.12.0.0.elf","lightning-2.1.2_gcc-6.4.0_x86_32_O2_liblightning.so.1.0.0.elf","libunistring-0.9.10_gcc-6.4.0_x86_32_O2_libunistring.so.2.1.0.elf","gsl-2.5_gcc-6.4.0_x86_32_O2_libgslcblas.so.0.0.0.elf","libtool-2.4.6_gcc-6.4.0_x86_32_O2_libltdl.so.7.3.1.elf","gmp-6.1.2_gcc-6.4.0_x86_32_O2_libgmp.so.10.3.2.elf","gdbm-1.15_gcc-6.4.0_x86_32_O2_libgdbm.so.6.0.0.elf","readline-7.0_gcc-6.4.0_x86_32_O2_libreadline.so.7.0.elf","osip-5.0.0_gcc-6.4.0_x86_32_O2_libosipparser2.so.12.0.0.elf","libiconv-1.15_gcc-6.4.0_x86_32_O2_libcharset.so.1.0.0.elf","gsasl-1.8.0_gcc-6.4.0_x86_32_O2_libgsasl.so.7.9.6.elf","gss-1.0.3_gcc-6.4.0_x86_32_O2_libgss.so.3.0.3.elf","glpk-4.65_gcc-6.4.0_x86_32_O2_libglpk.so.40.3.0.elf"])

    T = []
    R32 = []
    R64 = []
    RALL = []

    RO0 = []
    RO1 = []
    RO2 = []
    RO3 = []

    RCLANG = []
    RGCC   = []

    with open("A_MO", "rb") as f:
        E = pickle.load(f)
        S = [idS for idS in E]
        del E

    # ['recutils-1.7', 'clang-5.0', 'x86', '32', 'O1', 'librec.so.1.0.0.elf']
    for idS in S:
        t = idS.split("_")
        b = t[3]
        c = t[4]
        n = "_".join(t[5:])
        sample = (idS, "", c, n, "")
        if idS in targets:
            T += [sample]
        if b == "32":
            R32 += [sample]
        elif b == "64":
            R64 += [sample]

        if c == "O0":
            RO0 += [sample]
        elif c == "O1":
            RO1 += [sample]
        elif c == "O2":
            RO2 += [sample]
        elif c == "O3":
            RO3 += [sample]

        if "clang" in idS:
            RCLANG += [sample]
        elif "gcc" in idS:
            RGCC += [sample]
        RALL += [sample]

    run((T, RO0), "O0")
    run((T, RO1), "O1")
    run((T, RO2), "O2")
    run((T, RO3), "O3")
    run((T, RCLANG), "CLANG")
    run((T, RGCC), "GCC")
    run((T, R32), "32")
    run((T, R64), "64")
    run((T, RALL), "ALL")
