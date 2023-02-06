import pandas as pd

testfields = {}


with open("NORMAL_RUN_0.txt", "r") as f:
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
archs = ["arm","mips","x86","mipseb"]
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


#table.to_csv("SelectedNormal.csv", sep=';', encoding='utf-8')"""