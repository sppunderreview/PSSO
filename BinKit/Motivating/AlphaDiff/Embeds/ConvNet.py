# https://twelveand0.github.io/AlphaDiff-ASE2018-Appendix

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        
        self.relu = nn.ReLU()
        
        self.c1 = nn.Conv2d(1, 32, (3,3), stride=1, padding=1, dilation=1)
        self.b1 = nn.BatchNorm2d(32)

        self.c2 = nn.Conv2d(32, 32, (3,3), stride=1, padding=1, dilation=1)
        self.b2 = nn.BatchNorm2d(32)

        self.mp1 = nn.MaxPool2d((2, 2), stride=(2, 2))
        self.c3 = nn.Conv2d(32, 64, (3,3), stride=1, padding=1, dilation=1)
        self.b3 = nn.BatchNorm2d(64)

        self.c4 = nn.Conv2d(64, 64, (3,3), stride=1, padding=1, dilation=1)
        self.b4 = nn.BatchNorm2d(64)

        self.mp2 = nn.MaxPool2d((2, 2), stride=(2, 2))
        self.c5 = nn.Conv2d(64, 96, (3,3), stride=1, padding=1, dilation=1)
        self.b5 = nn.BatchNorm2d(96)

        self.c6 = nn.Conv2d(96, 96, (3,3), stride=1, padding=1, dilation=1)
        self.b6 = nn.BatchNorm2d(96)

        self.mp3 = nn.MaxPool2d((2, 2), stride=(2, 2))
        self.c7 = nn.Conv2d(96, 96, (3,3), stride=1, padding=1, dilation=1)
        self.b7 = nn.BatchNorm2d(96)

        self.c8 = nn.Conv2d(96, 96, (3,3), stride=1, padding=1, dilation=1)
        self.b8 = nn.BatchNorm2d(96)

        self.mp4 = nn.MaxPool2d((2, 2), stride=(2, 2))
        self.lin1 = nn.Linear(96,512,bias=True)
        self.lin2 = nn.Linear(18432,64,bias=True)


    def forward(self, x):
        x = self.c1(x)
        x = self.b1(x)

        x = self.relu(x)
        x = self.c2(x)
        x = self.b2(x)

        x = self.relu(x)
        x = self.mp1(x)
        x = self.c3(x)
        x = self.b3(x)

        x = self.relu(x)
        x = self.c4(x)
        x = self.b4(x)


        x = self.relu(x)
        x = self.mp2(x)
        x = self.c5(x)
        x = self.b5(x)

        x = self.relu(x)
        x = self.c6(x)
        x = self.b6(x)

        x = self.relu(x)
        x = self.mp3(x)
        x = self.c7(x)
        x = self.b7(x)

        x = self.relu(x)
        x = self.c8(x)
        x = self.b8(x)

        x = self.relu(x)        
        x = self.mp4(x)
        
        x = x.view(x.size(0),6,6,96)
        x = self.lin1(x)
        x = x.view(x.size(0),18432)
        return self.lin2(x)


