from __future__ import print_function
import argparse
import torch
import torch.optim as optim

from ConvNet import ConvNet
from AlphaDiffDataset import AlphaDiffDataset
from torch.utils.data import DataLoader


from random import randint

def train(args, model, device, train_loader, optimizer, epoch):
    model.train()

    totalLoss = 0
    for batch_idx, (pairsA, pairsB) in enumerate(train_loader):
        pairsA, pairsB = pairsA.to(device), pairsB.to(device)
        optimizer.zero_grad()


        # Positive samples
        embedsA = model(pairsA)
        embedsB = model(pairsB)        
        loss = torch.sum((embedsA - embedsB).norm(dim=1, p=2))
    
        # Negative sampling
        # Search for soft negative  I
        for i in range(embedsA.shape[0]):        
            for j in range(embedsB.shape[0]):                
                r = randint(0,embedsB.shape[0]-1)
                potentialLoss = (embedsA[i] - embedsB[r]).norm(dim=0, p=2)
                if potentialLoss > 1:
                    continue                
                loss += 1 - potentialLoss
                break
                
        # Search for soft negative  J
        for j in range(embedsB.shape[0]):     
            for i in range(embedsA.shape[0]): 
                r = randint(0,embedsA.shape[0]-1)
                potentialLoss = (embedsA[r] - embedsB[j]).norm(dim=0, p=2)
                if potentialLoss > 1:
                    continue                
                loss += 1 - potentialLoss
                break

        loss /= (embedsA.shape[0]*3)         
        loss.backward()
        optimizer.step()
        totalLoss += loss.item()

    print(totalLoss)
    
def main():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch Alpha Diff')
    parser.add_argument('--batch-size', type=int, default=100, metavar='N',
                        help='input batch size for training (default: 100)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    #parser.add_argument('--seed', type=int, default=1, metavar='S',
    #                    help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=1, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=True,
                        help='For Saving the current Model')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    #torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")
    print(device)

    dataset = AlphaDiffDataset()
    data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=8)

    
    model = ConvNet()
    model.load_state_dict(torch.load("cnn_12.pt"))
    model = model.to(device)
    optimizer = optim.RMSprop(model.parameters(),  lr=0.001, alpha=0.9, eps=1e-08, weight_decay=0, momentum=0, centered=False)
    optimizer.load_state_dict(torch.load("optim_12.pt"))
    
    trainable_params =  sum(p.numel() for p in model.parameters() if p.requires_grad)    
    print("# Trainable", trainable_params)
    
    for epoch in range(1 + 12, args.epochs + 1 + 12):
        train(args, model, device, data_loader, optimizer, epoch)
        model = model.to("cpu")
        if args.save_model:
            torch.save(model.state_dict(),     "cnn_"+str(epoch)+".pt")
            torch.save(optimizer.state_dict(), "optim_"+str(epoch)+".pt")
        model = model.to(device)


if __name__ == '__main__':
    main()
