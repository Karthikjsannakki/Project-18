

import torch
from nnet import activation

def cross_entropy_loss(outputs, labels):
    """Calculates cross entropy loss given outputs and actual labels
          H(y,p) = -sum (yi * pi ) of ith element 
    """    
# works properly
   
    m = labels.shape[0]
    p = outputs
    log_likelihood = -1*torch.log(p[range(m),labels])
    loss = torch.sum(log_likelihood) / m
    return loss.item()
    
    



def delta_cross_entropy_softmax(outputs, labels):
    """Calculates derivative of cross entropy loss (C) w.r.t. weighted sum of inputs (Z). 
       dL/do = pi - yi
    """
    
    m = labels.shape[0]
    grad = outputs
    
    grad[range(m),labels] -= torch.tensor(1.)

    grad = grad/m
    avg_grads = grad
    return avg_grads
    
    

if __name__ == "__main__":
    pass