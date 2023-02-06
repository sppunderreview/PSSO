import tensorflow as tf
import numpy as np
from datetime import datetime
from graphnnSiamese import graphnn
from utils import *
import os
import os
import pickle

nameXP = "total"

os.environ["CUDA_VISIBLE_DEVICES"] = "0"    # visible gpu device
NODE_FEATURE_DIM = 7 # feature dimension
EMBED_DIM = 64 # embedding dimension
EMBED_DEPTH = 2 # embedding network depth
OUTPUT_DIM = 64 # output layer dimension
ITERATION_LEVEL = 5 # iteration times
LEARNING_RATE = 1e-4 # learning rate
MAX_EPOCH = 50 # epoch number
BATCH_SIZE = 1 # batch size

LOAD_PATH = None # path for model loading, "#LATEST#" for the latest checkpoint
SAVE_PATH = "./saved_model_"+nameXP+"/graphnn-model" # path for model saving
LOG_PATH = None # path for training log

SHOW_FREQ = 1
TEST_FREQ = 1
SAVE_FREQ = 1

os.system("mkdir saved_model_"+nameXP)

FUNC_NAME_DICT = get_f_dict("./data/dataset.json")
Gs, classes =  read_graph("./data/dataset.json", FUNC_NAME_DICT, NODE_FEATURE_DIM)

print("{} graphs, {} functions".format(len(Gs), len(classes)))

perm = np.random.permutation(len(classes))
Gs_train, classes_train, Gs_dev, classes_dev, Gs_test, classes_test = partition_data(Gs,classes,[0.95,0.05,0.0], perm)

print("Train: {} graphs, {} functions".format(
        len(Gs_train), len(classes_train)))
print("Dev: {} graphs, {} functions".format(
        len(Gs_dev), len(classes_dev)))
print("Test: {} graphs, {} functions".format(
        len(Gs_test), len(classes_test)))

# Fix the pairs for validation
valid_epoch, valid_ids = generate_epoch_pair(Gs_dev, classes_dev, BATCH_SIZE, output_id=True)

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
gnn.init(LOAD_PATH, LOG_PATH)

# Train
auc, fpr, tpr, thres = get_auc_epoch(gnn, Gs_train, classes_train,
        BATCH_SIZE, load_data=valid_epoch)
gnn.say("Initial training auc = {0} @ {1}".format(auc, datetime.now()))
auc0, fpr, tpr, thres = get_auc_epoch(gnn, Gs_dev, classes_dev,
        BATCH_SIZE, load_data=valid_epoch)
gnn.say("Initial validation auc = {0} @ {1}".format(auc0, datetime.now()))

best_auc = 0
for i in range(1, MAX_EPOCH+1):
    l = train_epoch(gnn, Gs_train, classes_train, BATCH_SIZE)

    if (i % TEST_FREQ == 0):
        auc, fpr, tpr, thres = get_auc_epoch(gnn, Gs_dev, classes_dev,
                BATCH_SIZE, load_data=valid_epoch)
        gnn.say("Validation auc = {0} @ {1}".format(auc, datetime.now()))

        if auc > best_auc:
            path = gnn.save(SAVE_PATH+'_best')
            best_auc = auc
        
    if (i % SAVE_FREQ == 0):
        path = gnn.save(SAVE_PATH, i)

print(best_auc)
