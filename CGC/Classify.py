from Prototype import extractCallGraphs
    
def run(O):
    O0 = O[0]
    O1 = O[1]
    functionsDataS, graphPPredsS, graphPSuccsS, programsSNE = extractCallGraphs(O0)
    functionsDataT, graphPPredsT, graphPSuccsT, programsTNE = extractCallGraphs(O1)

import sys
sys.path.insert(0, "C:\\Users\\?\\Desktop\\BigVersions\\")
from makeBench import benchmark

P1D = benchmark("V0","V1")
P2D = benchmark("V2","V3")

run(P1D)
run(P2D)

