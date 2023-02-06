import numpy as np

from LoadBase import loadGraphs

def computeEmbedding(inputs):
    programs, programsExtern = loadGraphs(inputs)
    pV = {}
    for p in programs:
        pV[p] =  [programsExtern[p]]
    return pV
