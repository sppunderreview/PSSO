import torch
from torch.utils.data import Dataset
import numpy as np
import h5py

class AlphaDiffDataset(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        return 625318

    def open_hdf5(self):
        self.hf = h5py.File('/tmp/datasetAD.h5', 'r')

    def __del__(self):
        if hasattr(self, 'hf'):
            self.hf.close()

    def __getitem__(self, idx):
        if not hasattr(self, 'hf'):
            self.open_hdf5()
        pair = self.hf.get(str(idx))
        pair = np.array(pair)
        pair = torch.from_numpy(pair).float()
        return pair[0].unsqueeze(0), pair[1].unsqueeze(0)




