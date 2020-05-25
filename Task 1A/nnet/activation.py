
# NOTE: You can only use Tensor API of PyTorch


import torch

# Extra TODO: Document with proper docstring

def sigmoid(z):
    """Calculates sigmoid values for tensors which 1/(1+e^-input(i)) 
    """
    z = torch.tensor(z,dtype=torch.float)
    result = 1/(1+torch.exp(-z))
 #works   
    return result

# Extra TODO: Document with proper docstring
def delta_sigmoid(z):
    """Calculates derivative of sigmoid function

    """
    z = torch.tensor(z,dtype=torch.float)
    grad_sigmoid = sigmoid(z) * (1-sigmoid(z))
    return grad_sigmoid
#works
# Extra TODO: Document with proper docstring
def softmax(x):
    """Calculates stable softmax (minor difference from normal softmax) values for tensors

    """
    x = torch.tensor(x,dtype=torch.float)
    a={}
    label=0
    ps  = 0
    for i in range(x.shape[0]):
        ps   =  torch.exp(x[i])
        ps /= torch.sum(ps) 
        a[label]= ps ; label+=1
    
    total = torch.cat([a[i] for i in range(len(a))])
    result=total.reshape(x.size(0), x.size(1))
    stable_softmax = result
#works    
    return stable_softmax



if __name__ == "__main__":
    pass
