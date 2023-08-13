import pandas as pd

testfields = {}


with open("RESULTS.txt", "r") as f:
    for l in f.readlines():
        t = l.split(" ")
        m = t[0]        
        testfield = t[1]        
        st = testfield.split("_VS_")
        st = sorted(st)
        st = "_VS_".join(st)       
        acc = float(t[4])
        elapsed = float(t[5].strip())
        
        if not(st in testfields):
            testfields[st] = {}
        if not(m in testfields[st]):
            testfields[st][m] = []
        testfields[st][m] += [acc]  
        #SHAPE clang-7.0_VS_clang-4.0 4859 7520 0.6461436170212767 0.026812818487907977

averageSI = {}

for tf in testfields:
    for m in testfields[tf]:
        if not (m in averageSI):
            averageSI[m] = []
            
        if len(testfields[tf][m]) != 2:
            print("ALERT")
            
        testfields[tf][m] =  sum(testfields[tf][m])/len(testfields[tf][m])
        averageSI[m] += [testfields[tf][m]]
        testfields[tf][m] =  "{0:.2f}".format(testfields[tf][m])

for m in averageSI:
    print(m, sum(averageSI[m])/len(averageSI[m]))

"""
PSS 0.6207474158773809
PSSV16 0.6218435037364183
SHAPE 0.2959215644890439
BSIZE 0.17659854576639453
DSIZE 0.06511261507327554
SCG 0.5492785423558223
STRINGS 0.970185728855849
FUNCTIONSET 0.4910460563475201
MUTANTX 0.36461298371072565
LIBDX 0.8836835452526166
"""

selected = ["O0_VS_O3", "O2_VS_O3", "gcc-4.9.4_VS_gcc-8.2.0", "clang-4.0_VS_clang-7.0", "clang_VS_gcc"]
selected += ["clang-obfus-bcf_VS_normal","clang-obfus-fla_VS_normal","clang-obfus-sub_VS_normal","clang-obfus-all_VS_normal"]

archs = ["arm","mips","x86"]
for x in archs:
    for y in archs:
        if x >= y :
            continue
        selected += [x+"_VS_"+y]
selected += ["32_VS_64"]

testfieldsS = {}
for x in selected:
    x2 = x.replace("_", " ")
    x2 = x2.replace("VS", "vs")
    x2 = x2.replace("4.9.4","4")
    x2 = x2.replace("8.2.0","8")
    x2 = x2.replace("4.0","4")   
    x2 = x2.replace("7.0","7")
    x2 = x2.replace("clang-obfus-","")
    x2 = x2.replace(" vs normal", "")
    testfieldsS[x2] = testfields[x]
    
table = pd.DataFrame(testfieldsS)
print(table)

latex =  table.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

latex = latex.replace("PSS", "\\hline\n \PSS")
latex = latex.replace("SCG ", "{\\it ASCG} ")
latex = latex.replace("MUTANTX", "\\hline\n{\\it MutantX-S}")
latex = latex.replace("DSIZE", "$D_{size}$")
latex = latex.replace("BSIZE", "$B_{size}$")
latex = latex.replace("FUNCTIONSET", "\\hline\n{\\it FunctionSet}")
latex = latex.replace("SHAPE", "{\\it Shape}")
latex = latex.replace("STRINGS", "{\\it StringSet } ")
latex = latex.replace("LibDX", "{\\it LibDX } ")

print(latex)

"""PSSOH 

simCG 0.5958857111081636
simCFG 0.4241463430211706


\begin{tabular}{llllllllllllll}
\toprule
{} & O0 vs O3 & O2 vs O3 & gcc-4 vs gcc-8 & clang-4 vs clang-7 & clang vs gcc &   bcf &   fla &   sub &   all & arm vs mips & arm vs x86 & mips vs x86 & 32 vs 64 \\
\midrule
simCG  &     0.13 &     0.71 &           0.81 &               0.92 &         0.51 &  0.58 &  0.68 &  0.80 &  0.52 &        0.15 &       0.51 &        0.13 &     0.63 \\
simCFG &     0.08 &     0.34 &           0.60 &               0.74 &         0.25 &  0.20 &  0.18 &  0.66 &  0.16 &        0.33 &       0.37 &        0.40 &     0.48 \\
\bottomrule
\end{tabular}
"""