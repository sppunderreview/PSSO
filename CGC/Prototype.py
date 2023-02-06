from LoadBase import loadGraphs
import numpy as np
from copy import deepcopy

import random

def createClassTable(opcodes):
    opcodesTable = {'sub': 6, 'mov': 1, 'test': 5, 'jz': 10, 'call': 9, 'add': 6, 'retn': 9, 'push': 2, 'jmp': 9, 'xor': 7, 'cmp': 5, 'pop': 2, 'movsxd': 1, 'jle': 10, 'lea': 4, 'jg': 10, 'jnz': 10, 'and': 7, 'hlt': 12, 'jbe': 10, 'rep': 11, 'sar': 6, 'shr': 6, 'setz': 13, 'movaps': 1, 'ja': 10, 'setnz': 13, 'nop': 1, 'jb': 10, 'jnb': 10, 'movzx': 1, 'shl': 6, 'bt': 13, 'cmovnz': 1, 'cmovz': 1, 'js': 10, 'not': 7, 'div': 6, 'imul': 6, 'extrn': 1, 'or': 7, 'repne': 11, 'movsx': 1, 'sbb': 6, 'cdqe': 1, 'jl': 10, 'jge': 10, 'movdqu': 1, 'cmovb': 1, 'cmovnb': 1, 'xchg': 1, 'jns': 10, 'cqo': 1, 'idiv': 6, 'setnle': 13, 'movss': 1, 'ucomiss': 15, 'addss': 15, 'pxor': 7, 'cvtsi2ss': 15, 'divss': 15, 'cvttss2si': 15, 'mul': 6, 'subss': 15, 'mulss': 15, 'rol': 6, 'cdq': 1, 'setl': 13, 'cmovg': 1, 'cmova': 1, 'leave': 2, 'nop;': 1, 'jno': 10, 'neg': 6, 'cmovs': 1, 'cvtsi2sd': 1, 'addsd': 6, 'movsd': 1, 'mulsd': 6, 'divsd': 6, 'movapd': 1, 'endbr64': 10, 'bnd': 10, 'cmovbe': 1, 'movdqa': 1, 'movups': 1, 'repe': 11, 'setnbe': 13, 'setbe': 13, 'movq': 1, 'punpcklqdq': 6, 'pcmpeqb': 13, 'pand': 7, 'punpckhbw': 6, 'punpcklbw': 6, 'punpckhwd': 6, 'punpcklwd': 6, 'punpckldq': 6, 'punpckhdq': 6, 'paddq': 6, 'psrldq': 6, 'cmovge': 1, 'cmovle': 1, 'cmovns': 1, 'cld': 5, 'pcmpgtb': 5, 'pcmpgtw': 5, 'paddd': 6, 'movd': 1, 'cmovl': 1, 'pandn': 7, 'comisd': 15, 'movhps': 1, 'setle': 13, 'setnl': 13, 'setnb': 13, 'psubq': 6, 'jo': 10, 'ror': 6, 'setb': 13, 'adc': 6, 'ucomisd': 15, 'jp': 10, 'cvttsd2si': 15, 'subsd': 6, 'btc': 13, 'ud2': 1, 'setnp': 13, 'maxsd': 15, 'pshufd': 6, 'paddw': 6, 'shufps': 6, 'packuswb': 1, 'movsb': 1, 'andpd': 7, 'andnpd': 7, 'cmpnlesd': 5, 'orpd': 7, 'por': 7, 'psubd': 6, 'xorpd': 7, 'cmpltsd': 5, 'setp': 13, 'fld': 15, 'fstp': 15, 'jnp': 10, 'fldz': 15, 'fcomip': 15, 'movmskpd': 1, 'fucomip': 15, 'comiss': 15, 'pcmpeqd': 5, 'sqrtsd': 15, 'pcmpgtd': 5, 'paddb': 6, 'shufpd': 6, 'psrlw': 6, 'psubusb': 6, 'seto': 5, 'bswap': 1, 'cwde': 1, 'cvtss2sd': 15, 'fadd': 6, 'cvtsd2ss': 15, 'movsq': 1, 'pmuludq': 6, 'psllq': 6, 'psrad': 6, 'pslld': 6, 'rdsspq': 5, 'incsspq': 5, 'inc': 5, 'lock': 14, 'bts': 13, 'minsd': 15, 'bsr': 13, 'cmovp': 1, 'cmplesd': 5, 'psrld': 6, 'shld': 6, 'punpckhqdq': 6, 'endbr64;': 10, 'prefetcht0': 14, 'tzcnt': 13, 'psrlq': 6, 'cmovo': 1, 'cmovno': 1, 'bsf': 13, 'shrd': 6, 'unpcklpd': 1, 'stmxcsr': 1, 'ldmxcsr': 1, 'fild': 1, 'movupd': 1, 'addpd': 6, 'subpd': 6, 'mulpd': 6, 'movlpd': 1, 'cvttpd2dq': 15, 'maxss': 15, 'minss': 15, 'cmpnltsd': 5, 'movhpd': 1, 'unpckhpd': 1, 'divpd': 6, 'unpcklps': 1, 'movlhps': 1, 'movhlps': 1, 'psllw': 6, 'pmullw': 6, 'pmulhw': 6, 'psubw': 6, 'cbw': 1, 'dec': 5, 'andps': 6, 'xorps': 7, 'btr': 13, 'mfence': 14, 'fnstcw': 1, 'fldcw': 1, 'fxch': 1, 'fucomi': 1, 'movsw': 1, 'pcmpeqw': 5, 'fistp': 1, 'fsubp': 6, 'faddp': 6, 'fdivp': 6, 'fmulp': 6, 'fld1': 15, 'fchs': 6, 'fdivrp': 6, 'fsubrp': 6, 'fldz;': 15, 'fsub': 6, 'fmul': 6, 'fdiv': 6, 'fchs;': 6, 'fdivr': 6, 'fsubr': 6, 'sets': 13, 'orps': 15, 'cpuid': 14, 'int': 14, 'pause': 14, 'haddps': 15, 'mulps': 15, 'vmovss': 15, 'vbroadcastss': 15, 'vmovaps': 15, 'vmovups': 15, 'vinsertf128': 15, 'vblendps': 15, 'vshufps': 15, 'vmulps': 15, 'vperm2f128': 15, 'vaddps': 15, 'vextractf128': 15, 'vmulss': 15, 'vaddss': 15, 'addps': 15, 'psraw': 6, 'cvtdq2ps': 15, 'unpckhps': 15, 'maxps': 15, 'minps': 15, 'cvtps2dq': 15, 'packssdw': 1, 'packsswb': 1, 'pinsrw': 1, 'pushfq': 2, 'popfq': 2, 'xgetbv': 1, 'emms': 7, 'prefetchnta': 14, 'movntps': 1, 'pmaddwd': 6, 'pshuflw': 6, 'pshufhw': 6, 'movntdq': 1, 'pavgb': 6, 'cmpnless': 15, 'andnps': 15, 'pextrw': 1, 'sqrtss': 15, 'cmpltss': 15, 'vzeroupper': 6, 'retn;': 10, 'maxpd': 15, 'cvtdq2pd': 15, 'cmpltpd': 15, 'minpd': 15, 'cvtpd2ps': 15, 'subps': 15, 'divps': 15, 'movlps': 15, 'pmulhuw': 1, 'movddup': 15, 'cvttps2dq': 15, 'stosd': 1, 'fxam': 15, 'fnstsw': 1, 'cmpnltss': 15, 'cvtps2pd': 15, 'rdrand': 14, 'loop': 11, 'pshufb': 6, 'palignr': 1, 'pslldq': 6, 'pclmulqdq': 6, 'aesenc': 6, 'aesenclast': 6, 'aesdec': 6, 'aesdeclast': 6, 'pextrd': 1, 'pinsrd': 1, 'aesimc': 6, 'aeskeygenassist': 6, 'cvtpd2dq': 15, 'sha1msg1': 6, 'sha1rnds4': 6, 'sha1nexte': 6, 'sha1msg2': 6, 'vmovdqa': 1, 'vmovdqu': 1, 'vpshufb': 6, 'vpaddd': 6, 'vpalignr': 1, 'vpsrldq': 6, 'vpxor': 7, 'vpsrld': 6, 'vpslldq': 6, 'vpor': 7, 'vpslld': 6, 'vinserti128': 1, 'rorx': 7, 'andn': 7, 'sha256rnds2': 6, 'sha256msg1': 6, 'sha256msg2': 6, 'vpshufd': 6, 'vpsrlq': 6, 'vpaddq': 6, 'vprotq': 6, 'vpsllq': 6, 'vpcmpgtd': 7, 'vpand': 7, 'vpunpckhqdq': 1, 'vpclmulqdq': 6, 'vxorps': 7, 'vmovq': 1, 'mulx': 6, 'adcx': 6, 'adox': 6, 'jrcxz': 10, 'vpbroadcastq': 1, 'vpmuludq': 6, 'vpermq': 6, 'vpblendd': 1, 'vmovd': 1, 'vzeroall': 6, 'vpermd': 6, 'vpbroadcastd': 1, 'vpcmpeqd': 7, 'vextracti128': 1, 'shlx': 6, 'shrx': 6, 'ht': 12, 'vpinsrd': 1, 'vpunpckldq': 1, 'vpandn': 7, 'movbe': 1, 'vaesenc': 6, 'vaesenclast': 6, 'vprotd': 1, 'vpinsrq': 1, 'vpextrq': 1, 'vaesdec': 6, 'vaesdeclast': 6, 'vpaddb': 6, 'rdtsc': 14, 'fcomi': 15}
    toDo = 0
    for op in opcodes:
        if not(op in opcodesTable):
            toDo += 1
    if toDo == 0:
        return opcodesTable

    print("START TO CLASSIFY",  toDo)
    
    for op in opcodes:
        if op in opcodesTable:
            continue
        print(op)
        c = input()
        while (not(c in [str(i) for i in range(1,16)])):
            c = input()
        opcodesTable[op] = int(c)
        print("OK")
    
    print(opcodesTable)
    return opcodesTable
        
        

def extractCallGraphs(inputs,):
    functionsData, graphPPreds, graphPSuccs, programs = loadGraphs(inputs)
        
    opcodes = {}
    for p in functionsData:
        for f in functionsData[p]:
            for op in functionsData[p][f]["instructions"]: 
                opcodes[op] = True
    
    opcodesClasses = createClassTable(opcodes)
    
    for p in functionsData:
        for f in functionsData[p]:
            vector = [0 for i in range(15)]
            for op in functionsData[p][f]["instructions"]: 
                if op in ["extern","nop","nop;","ud2"]:
                    continue
                vector[opcodesClasses[op]-1] += 1
            color  = [0 for i in range(15)]
            for i in range(15):
                if vector[i] > 0:
                    color[i] = 1
                else:
                    color[i] = 0
            del functionsData[p][f]["instructions"]
            functionsData[p][f]["color"] = color
            functionsData[p][f]["vector"] = np.array(vector)
        
    return functionsData, graphPPreds, graphPSuccs, programs

def extractExternalFunction(functionD):
    external = []
    for f in functionD:
        if functionD[f]["extern"] == False:
            continue
        external += [f]
    return external

def colorSimilarity(sColor, tColor, sVector, tVector):
    for i in range(len(sColor)):
        if sColor[i] != tColor[i]:
            return 0
    return np.dot(sVector, tVector)/(np.linalg.norm(sVector)*np.linalg.norm(tVector))

def lenSimilarity(sL, tL):
    if sL > tL:
        return sL/tL
    return tL/sL

def degreeSimilarity(sD, tD):
    if sD == tD:
        return 1
    return 1/(abs(sD-tD))

def relaxedColorSimilarity(sVector, tVector):
    return np.dot(sVector, tVector)/(np.linalg.norm(sVector)*np.linalg.norm(tVector))
    

def successorMatch(comVertex, U_S_V, U_T_V, succS, succT, functionS, functionT):
    alpha = 0.50
    queueCom = deepcopy(comVertex)
    
    while (len(queueCom) > 0):
        (u,v) = queueCom[-1]
        queueCom = queueCom[:-1]
        
        if not(u in succS):
            continue
            
        for uS in succS[u]:
            if not(uS in U_S_V):
                continue
            if not(v in succT):
                continue
            for uT in succT[v]:
                if not(uT in U_T_V):
                    continue
                colorS = relaxedColorSimilarity(functionS[uS]["vector"], functionT[uT]["vector"])
                if colorS >= alpha:
                    comVertex += [(uS, uT)]                    
                    queueCom += [(uS, uT)]
                    if uS in U_S_V:
                        del U_S_V[uS]
                    if uT in U_T_V:
                        del U_T_V[uT]
                    
    return comVertex
                
    

def computesComEdges(comVertex, succS, succT):  
    comVertexD = {}
    for (u,v) in comVertex:
        comVertexD[str((u,v))] = True
    comE = 0

    for u in succS:
        for v in succS[u]:
            isIn = False
            for uT in succT:
                if isIn:
                    break
                for vT in succT[uT]:
                    if (str((u, uT)) in comVertexD) and (str((v, vT)) in comVertexD): 
                        isIn = True
                        break
            if isIn:
                comE += 1
    return comE

def functionCallSimilarity(functionS, predS, succS, neS, functionT, predT, succT, neT):
    alpha = 0.45  #0.98
    beta  = 0.1  #0.83
    gamma = 0.3  #0.5
    
    # Matching external functions
    externalFunctionS = extractExternalFunction(functionS)
    externalFunctionT = extractExternalFunction(functionT)
    
    U_S_V = {}
    for f in functionS:
        U_S_V[f] = True
    U_T_V = {}
    for f in functionT:
        U_T_V[f] = True
    
    comVertex = []
    
    for u in externalFunctionS:
        for v in externalFunctionT:
            if functionS[u]["name"] == functionT[v]["name"]:
                comVertex += [(u,v)]
                if u in U_S_V:
                    del U_S_V[u]
                if v in U_T_V:
                    del U_T_V[v]
    
    # Matching local functions by the same called external functions
    if len(comVertex) > 0:
        for uS in functionS:
            if not(uS in U_S_V):
                continue
            for uT in functionT:
                if not(uT in U_T_V):
                    continue
                if len(functionS[uS]["externalCalls"].intersection(functionT[uT]["externalCalls"])) >= 2 :
                    comVertex += [(uS,uT)]
                    if uS in U_S_V:
                        del U_S_V[uS]
                    if uT in U_T_V:
                        del U_T_V[uT]

    # Matching local functions according to opcodes
    for uS in functionS:
        if not(uS in U_S_V):
            continue
        for uT in functionT:
            if not(uT in U_T_V):
                continue
            
            colorS = colorSimilarity(functionS[uS]["color"], functionT[uT]["color"], functionS[uS]["vector"], functionT[uT]["vector"])
            lenS = lenSimilarity(functionS[uS]["len"], functionT[uT]["len"])
            degreeS = degreeSimilarity(functionS[uS]["degree"], functionT[uT]["degree"])
            
            if colorS >= alpha and lenS >= beta and degreeS >= gamma:
                comVertex += [(uS,uT)]
                if uS in U_S_V:
                    del U_S_V[uS]
                if uT in U_T_V:
                    del U_T_V[uT]
    
    # Matching local functions by matched neighborhood
    
    comVertex = successorMatch(comVertex, U_S_V, U_T_V, succS, succT, functionS, functionT)
    comVertex = successorMatch(comVertex, U_S_V, U_T_V, predS, predT, functionS, functionT)
    
    # Calculating Similarity
    comEdges = computesComEdges(comVertex, succS, succT)
    
    return (2*comEdges)/(neS+neT)
    
    
