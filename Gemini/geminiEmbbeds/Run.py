import tensorflow as tf
from graphnnSiamese import graphnn
from utils import *

import os
from os import listdir
from os.path import isfile, join

import pickle

def extractVectors(nameDS):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"    # visible gpu device
    NODE_FEATURE_DIM = 7 # feature dimension
    EMBED_DIM = 64 # embedding dimension
    EMBED_DEPTH = 2 # embedding network depth
    OUTPUT_DIM = 64 # output layer dimension
    ITERATION_LEVEL = 5 # iteration times
    LEARNING_RATE = 1e-4 # learning rate
    BATCH_SIZE = 1 # batch size

    # Model
    gnn = graphnn(
            N_x = NODE_FEATURE_DIM,
            Dtype = tf.float32,
            N_embed = EMBED_DIM,
            depth_embed = EMBED_DEPTH,
            N_o = OUTPUT_DIM,
            ITER_LEVEL = ITERATION_LEVEL,
            lr = LEARNING_RATE
        )
    gnn.init("saved_model_total/graphnn-model_best", None)

    # Process the testing graphs
    DATA_FILE_NAME = "./data/"+nameDS+"/"
    F_NAME = [DATA_FILE_NAME+f for f in listdir(DATA_FILE_NAME) if isfile(join(DATA_FILE_NAME, f))]
    
    i = 0
    for x in F_NAME:
        FUNC_NAME_DICT = get_f_dict([x])
        Gs, classes = read_graph([x], FUNC_NAME_DICT, NODE_FEATURE_DIM)
        print("{} test graphs, {} functions".format(len(Gs), len(classes)))

        test_epoch, test_ids = generate_epoch_pair(Gs, classes, BATCH_SIZE, output_id=True)
        vectors = get_vectors(gnn, BATCH_SIZE, test_epoch, FUNC_NAME_DICT)
        with open("vecById/"+nameDS+"_"+str(i), 'wb') as f:
            pickle.dump(vectors, f)
        i += 1
        
extractVectors("CO")
extractVectors("CV")
extractVectors("BO")
extractVectors("BV")
extractVectors("UV")
extractVectors("UO")
