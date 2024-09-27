import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import random


# read the data
words = open('names.txt').read().splitlines()

# build mapping and character vocabulary
chars = sorted(list(set(''.join(words))))
stoi = {s:i+1 for i,s in enumerate(chars)}
stoi['.'] = 0 # special character for end of word
itos = {i:s for s,i in stoi.items()}


# build the dataset
def build_dataset(words, block_size):
    ''' Builds the dataset (i.e. a list of context and target pairs) of block size number of characters from the list of words.
    Args:
    words: list of strings
    block_size: int, number of characters in the context
    Returns:
    X: torch tensor of shape (N, block_size), where N is the number of characters in the dataset
    Y: torch tensor of shape (N,), where each element is the index of the target character in the vocabulary
    '''

    X, Y = [], []
    for w in words:

        context = [0] * block_size # context is a list of 0s of length block_size
        for ch in w + '.':
            ix = stoi[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix] # update context with the next character

    X = torch.tensor(X)
    Y = torch.tensor(Y)
    # print(X.shape, Y.shape)
    return X, Y


def train_model(X, Y, iterations, lr, parameters):
    print('Training ...')

    for i in range(iterations):

        # build minibatch
        ix = torch.randint(0, X.shape[0], (32,))

        # forward pass
        emb = C[X[ix]] # embed the input as a tensor of shape 32, 3, 2
        h = torch.tanh((emb.view(-1, 6)) @ w1 + b1) ## tanh is making values betweeen -1 and 1
        logits = h @ w2 + b2

        loss = F.cross_entropy(logits, Y[ix])

        # backward pass
        for p in parameters:
            p.requires_grad = True
            p.grad = None
        loss.backward()

        # update
        for p in parameters:
            p.data -= lr * p.grad

        # print(loss.item())
    
    print('Loss after', i, 'iterations:', loss.item())
    return loss.item()
    

def test_learning_rate(X, Y, lrs, parameters):
    '''
    Function to test the learning rates effect on the loss and return the best learning rate

    Args:
    X: torch tensor of shape (N, block_size), where N is the number of characters in the dataset
    Y: torch tensor of shape (N,), where each element is the index of the target character in the vocabulary
    lrs: list of learning rates to test
    parameters: list of parameters to update

    Returns:
    best_lr: the best learning rate
    '''
    lri, lossi = [], []

    for i in range(len(lrs)):

        # build minibatch
        ix = torch.randint(0, X.shape[0], (32,))

        # forward pass
        emb = C[X[ix]] # embed the input as a tensor of shape 32, 3, 2
        h = torch.tanh((emb.view(-1, 6)) @ w1 + b1) ## tanh is making values betweeen -1 and 1
        logits = h @ w2 + b2
        loss = F.cross_entropy(logits, Y[ix])

        # backward pass
        for p in parameters:
            p.requires_grad = True
            p.grad = None
        loss.backward()

        # update
        lr = lrs[i]
        # lr = 0.01
        for p in parameters:
            p.data -= lr * p.grad

        # track statistics
        lri.append(lre[i])
        lossi.append(loss.item())

    plt.plot(lri, lossi)    
    plt.show()
        
    best_lr = lrs[np.argmin(lossi)].item()
    print('Minimum loss is:', min(lossi), 'at learning rate:', lrs[np.argmin(lossi)].item())

    return best_lr





def name_maker(block_size):
     
    out = []
    context = [0] * block_size
    while True:
        emb = C[torch.tensor(context)]
        h = torch.tanh((emb.view(1, -1) @ w1 + b1))
        logits = h @ w2 + b2
        p = F.softmax(logits, 1)
        ix = torch.multinomial(p, 1).item()
        context = context[1:] + [ix]
        out.append(ix)

        if ix == 0: # end of name
            break
        
    return ''.join(itos[i] for i in out[:-1])

###################################################

# Initialise parameters
g = torch.Generator().manual_seed(2147483647)
C = torch.randn((27,2), generator=g, requires_grad=True)  # Set requires_grad=True directly here
w1 = torch.randn((6,100), generator=g, requires_grad=True)
b1 = torch.randn((100), generator=g, requires_grad=True)
w2 = torch.randn((100,27), generator=g, requires_grad=True)
b2 = torch.randn((27), generator=g, requires_grad=True)
parameters = [C, w1, b1, w2, b2]

# s = sum(p.nelement() for p in parameters)
# print('Number of parameters:', s)



# shuffle the words and split into train, dev, test
random.seed(42)
random.shuffle(words)
n1 = int(0.8*len(words))
n2 = int(0.9*len(words))

# build the model
Xtr, Ytr = build_dataset(words[:n1], 3)
Xdev, Ydev = build_dataset(words[n1:n2], 3)
Xte, Yte = build_dataset(words[n2:], 3)

# print(Xtr.shape, Ytr.shape)



# train the model
lre = torch.linspace(-3, 1, 1000)
# print(lre)
lrs = 10**lre
# print(lrs)

# lr = test_learning_rate(Xtr, Ytr, lrs, parameters) # return best learning rate

lr = 0.001
train_model(Xtr, Ytr, 10000, lr, parameters)

for i in range(10):
    print(name_maker(3)) # generate a name
