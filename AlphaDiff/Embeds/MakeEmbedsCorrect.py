import numpy as np
from Prototype import computeEmbedding
import time

import pickle

def run(O, folder):
    embeds = computeEmbedding(O)
    
    with open(folder+"/vecById", "wb") as f:
        pickle.dump(embeds,f)
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 
    from correctBenchBO import readToCorrect
    
    run(readToCorrect(),"BOC")