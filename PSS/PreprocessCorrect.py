import sys
sys.path.insert(0, "????") # PSS_PATH_BASIC_BO 

from Prototype import computeEmbedding
import pickle

#from makeBenchBO import readAllSamples as allBO
from correctBenchBO import readToCorrect

# Old and useless now correction

embedsOC = computeEmbedding(readToCorrect())    
with open("A_BO_C", "wb") as f:
    pickle.dump(embedsOC, f)
