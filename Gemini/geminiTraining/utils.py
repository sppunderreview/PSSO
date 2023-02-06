import numpy as np
#import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve
from graphnnSiamese import graphnn
import json

import matplotlib.pyplot as plt

def get_f_dict(path):
    name_num = 0
    name_dict = {}
    with open(path) as inf:
        for line in inf:
            g_info = json.loads(line.strip())
            nameF = g_info['src']+"_"+g_info['fname']
            if (nameF not in name_dict):
                name_dict[nameF] = name_num
                name_num += 1
    return name_dict

class graph(object):
    def __init__(self, node_num = 0, label = None, name = None):
        self.node_num = node_num
        self.label = label
        self.name = name
        self.features = []
        self.succs = []
        self.preds = []
        if (node_num > 0):
            for i in range(node_num):
                self.features.append([])
                self.succs.append([])
                self.preds.append([])
                
    def add_node(self, feature = []):
        self.node_num += 1
        self.features.append(feature)
        self.succs.append([])
        self.preds.append([])
        
    def add_edge(self, u, v):
        self.succs[u].append(v)
        self.preds[v].append(u)

    def toString(self):
        ret = '{} {}\n'.format(self.node_num, self.label)
        for u in range(self.node_num):
            for fea in self.features[u]:
                ret += '{} '.format(fea)
            ret += str(len(self.succs[u]))
            for succ in self.succs[u]:
                ret += ' {}'.format(succ)
            ret += '\n'
        return ret

        
def read_graph(path, FUNC_NAME_DICT, FEATURE_DIM):
    graphs = []
    classes = []
    if FUNC_NAME_DICT != None:
        for f in range(len(FUNC_NAME_DICT)):
            classes.append([])

    with open(path) as inf:
        for line in inf:
            g_info = json.loads(line.strip())
            label = FUNC_NAME_DICT[g_info['src']+"_"+g_info['fname']]
            classes[label].append(len(graphs))
            cur_graph = graph(g_info['n_num'], label, g_info['src']) # NAME HERE FOR RETRIEVAL
            for u in range(g_info['n_num']):
                cur_graph.features[u] = np.array(g_info['features'][u]).astype(float)
                for v in g_info['succs'][u]:
                    cur_graph.add_edge(u, v)
            graphs.append(cur_graph)

    return graphs, classes


def partition_data(Gs, classes, partitions, perm):
    C = len(classes)
    st = 0.0
    ret = []
    for part in partitions:
        cur_g = []
        cur_c = []
        ed = st + part * C
        for cls in range(int(st), int(ed)):
            prev_class = classes[perm[cls]]
            cur_c.append([])
            for i in range(len(prev_class)):
                cur_g.append(Gs[prev_class[i]])
                cur_g[-1].label = len(cur_c)-1
                cur_c[-1].append(len(cur_g)-1)

        ret.append(cur_g)
        ret.append(cur_c)
        st = ed

    return ret


def generate_epoch_pair(Gs, classes, M, output_id = False, load_id = None):
    epoch_data = []
    id_data = []   # [ ([(G0,G1),(G0,G1), ...], [(G0,H0),(G0,H0), ...]), ... ]

    if load_id is None:
        st = 0
        while st < len(Gs):
            if output_id:
                X1, X2, m1, m2, y, pos_id, neg_id = get_pair(Gs, classes,
                        M, st=st, output_id=True)
                id_data.append( (pos_id, neg_id) )
            else:
                X1, X2, m1, m2, y = get_pair(Gs, classes, M, st=st)
            epoch_data.append( (X1,X2,m1,m2,y) )
            st += M
    else:   ## Load from previous id data
        id_data = load_id
        for id_pair in id_data:
            X1, X2, m1, m2, y, = get_pair(Gs, classes, M, load_id=id_pair)
            epoch_data.append( (X1, X2, m1, m2, y) )

    if output_id:
        return epoch_data, id_data
    else:
        return epoch_data


def get_pair(Gs, classes, M, st = -1, output_id = False, load_id = None):
    if load_id is None:
        C = len(classes)

        if (st + M > len(Gs)):
            M = len(Gs) - st
        ed = st + M

        pos_ids = [] # [(G_0, G_1)]
        neg_ids = [] # [(G_0, H_0)]

        for g_id in range(st, ed):
            g0 = Gs[g_id]
            cls = g0.label
            tot_g = len(classes[cls])
            if (len(classes[cls]) >= 2):
                g1_id = classes[cls][np.random.randint(tot_g)]
                while g_id == g1_id:
                    g1_id = classes[cls][np.random.randint(tot_g)]
                pos_ids.append( (g_id, g1_id) )

            cls2 = np.random.randint(C)
            while (len(classes[cls2]) == 0) or (cls2 == cls):
                cls2 = np.random.randint(C)

            tot_g2 = len(classes[cls2])
            h_id = classes[cls2][np.random.randint(tot_g2)]
            neg_ids.append( (g_id, h_id) )
    else:
        pos_ids = load_id[0]
        neg_ids = load_id[1]
        
    M_pos = len(pos_ids)
    M_neg = len(neg_ids)
    M = M_pos + M_neg

    maxN1 = 0
    maxN2 = 0
    for pair in pos_ids:
        maxN1 = max(maxN1, Gs[pair[0]].node_num)
        maxN2 = max(maxN2, Gs[pair[1]].node_num)
    for pair in neg_ids:
        maxN1 = max(maxN1, Gs[pair[0]].node_num)
        maxN2 = max(maxN2, Gs[pair[1]].node_num)

    feature_dim = len(Gs[0].features[0])
    X1_input = np.zeros((M, maxN1, feature_dim))
    X2_input = np.zeros((M, maxN2, feature_dim))
    
    node1_mask = np.zeros((M, maxN1, maxN1))
    node2_mask = np.zeros((M, maxN2, maxN2))
    y_input = np.zeros((M))
    
    for i in range(M_pos):
        y_input[i] = 1
        
        g1 = Gs[pos_ids[i][0]]
        g2 = Gs[pos_ids[i][1]]
        for u in range(g1.node_num):
            X1_input[i, u, :] = np.array( g1.features[u] )
            for v in g1.succs[u]:
                node1_mask[i, u, v] = 1
        for u in range(g2.node_num):
            X2_input[i, u, :] = np.array( g2.features[u] )
            for v in g2.succs[u]:
                node2_mask[i, u, v] = 1
        
    for i in range(M_pos, M_pos + M_neg):
        y_input[i] = -1
        g1 = Gs[neg_ids[i-M_pos][0]]
        g2 = Gs[neg_ids[i-M_pos][1]]
        for u in range(g1.node_num):
            X1_input[i, u, :] = np.array( g1.features[u] )
            for v in g1.succs[u]:
                node1_mask[i, u, v] = 1
        for u in range(g2.node_num):
            X2_input[i, u, :] = np.array( g2.features[u] )
            for v in g2.succs[u]:
                node2_mask[i, u, v] = 1
    if output_id:
        return X1_input,X2_input,node1_mask,node2_mask,y_input,pos_ids,neg_ids
    else:
        return X1_input,X2_input,node1_mask,node2_mask,y_input


def train_epoch(model, graphs, classes, batch_size, load_data=None):
    print("GENERATE PAIR")
    if load_data is None:
        epoch_data = generate_epoch_pair(graphs, classes, batch_size)
    else:
        epoch_data = load_data

    print("START TRAIN")
    perm = np.random.permutation(len(epoch_data))   #Random shuffle

    cum_loss = 0.0
    for index in perm:
        cur_data = epoch_data[index]
        X1, X2, mask1, mask2, y = cur_data
        loss = model.train(X1, X2, mask1, mask2, y)
        cum_loss += loss

    return cum_loss / len(perm)


def get_auc_epoch(model, graphs, classes, batch_size, load_data=None):
    tot_diff = []
    tot_truth = []

    if load_data is None:
        epoch_data= generate_epoch_pair(graphs, classes, batch_size)
    else:
        epoch_data = load_data


    for cur_data in epoch_data:
        X1, X2, m1, m2,y  = cur_data
        diff = model.calc_diff(X1, X2, m1, m2)

        tot_diff += list(diff)
        tot_truth += list(y > 0)


    diff = np.array(tot_diff)
    truth = np.array(tot_truth)

    fpr, tpr, thres = roc_curve(truth, (1-diff)/2)
    model_auc = auc(fpr, tpr)
    

    return model_auc, fpr, tpr, thres
    
"""
def get_vectors(model, batch_size, data, dictF):
    reverseFID = {}
    for x in dictF:
        reverseFID[dictF[x]] = x 
        
    vectors = {}
    
    for cur_data in data:
        X1, X2, m1, m2,y, X1F, _  = cur_data
        vec = model.get_embed(X1, m1)
        
        for i in range(len(X1F)):
            nameP = X1F[i][0]
            nameF = reverseFID[X1F[i][1]]
            vectors[nameP+"_"+nameF] = vec[i]
    return vectors"""
