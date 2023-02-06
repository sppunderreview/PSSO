import os

import cv2
import h5py

import random
from tqdm import tqdm

"""

def loadTensor(path):
    return cv2.imread(path,0) 

def loadPair(path):        
    pairA = loadTensor(path+"##A.jpeg")
    pairB = loadTensor(path+"##B.jpeg")
    return (pairA, pairB)
    
pathDataset = "C:\\Users\\?\\Desktop\\alphadiff-dataset-master\\dataset\\data"

# 25%
# Compressé   =>  1 Go
# Décompressé => 50 Go

h5f = h5py.File('datasetAD.h5', 'w')

p = 0
for o in tqdm(os.listdir(pathDataset)):
    lP = os.path.join(pathDataset, o)
    if os.path.isdir(lP):
        listPairs = set()
        for o2 in os.listdir(lP):
            if len(o2) >= 5 and o2[-5:] == ".jpeg":
                oPath = o2.replace("##A.jpeg","").replace("##B.jpeg","")
                listPairs.add(oPath)        
        for pathPair in listPairs:
            if random.random() < 0.75:
                continue
            h5f.create_dataset(str(p), data=loadPair(os.path.join(lP, pathPair)))
            p += 1    

print("# pairs", p)
h5f.close()
"""

# 625 318 pairs