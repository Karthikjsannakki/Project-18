
# NOTE: You can only use Tensor API of PyTorch

import torch

# Extra TODO: Document with proper docstring
def mbgd(weights, biases, dw1, db1, dw2, db2, dw3, db3, lr):
    """Mini-batch gradient descent
    
    
    """
    
#works properly    
    
    new_weights={}   
    new_biases ={}
    new_weights['w1'] =   weights['w1'] - lr * dw1
    new_weights['w2'] =   weights['w2'] - lr * dw2
    new_weights['w3'] =   weights['w3'] - lr * dw3
    new_biases['b1'] =    biases['b1'] - lr * db1
    new_biases['b2'] =    biases['b2'] - lr * db2
    new_biases['b3'] =    biases['b3'] - lr * db3 
    return new_weights, new_biases

if __name__ == "__main__":
    pass