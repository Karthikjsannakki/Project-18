
# Homecoming (eYRC-2018): Task 1A
# Build a Fully Connected 2-Layer Neural Network to Classify Digits

# NOTE: You can only use Tensor API of PyTorch

from nnet import model
import torch
import torchvision as tv


# TODO: import torch and torchvision libraries
# We will use torchvision's transforms and datasets


# TODO: Defining torchvision transforms for preprocessing


#transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),torchvision.transforms.Normalize((0.1307,), (0.3081,))])

#transform = tv.transforms.Compose([tv.transforms.ToTensor()])
transform  = tv.transforms.Compose([tv.transforms.Grayscale(num_output_channels=1),
                                    tv.transforms.ToTensor(), 
                                    tv.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# TODO: Using torchvision datasets to load MNIST

train_dataset = tv.datasets.MNIST(root='./mnist/', train=True, transform=transform, download=True)
test_dataset = tv.datasets.MNIST(root='./mnist/', train=False, transform=transform, download=True)


# TODO: Use torch.utils.data.DataLoader to create loaders for train and test

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=4, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=4, shuffle=True)


# NOTE: Use training batch size = 4 in train data loader.



# NOTE: Don't change these settings
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# NOTE: Don't change these settings
# Layer size
N_in = 28 * 28 # Input size
N_h1 = 256 # Hidden Layer 1 size
N_h2 = 256 # Hidden Layer 2 size
N_out = 10 # Output size
# Learning rate
lr = 0.001
debug = False

# init model

net = model.FullyConnected(N_in, N_h1, N_h2, N_out, device=device)

# TODO: Define number of epochs
N_epoch = 5 # Or keep it as is

print("reached here")
# TODO: Training and Validation Loop
# >>> for n epochs
for i in range(N_epoch):
   
### >>> for all mini batches
    for batch_index, (inputs1, labels1) in enumerate(train_loader):     
        trainer_input = inputs1.view( inputs1.size(0) , inputs1.size(2)*inputs1.size(3))
        
#### >>> net.train(...)
        creloss, accuracy, outputs=net.train(trainer_input, labels1,lr,debug)
        print("trainning",batch_index,creloss,accuracy)
### at the end of each training epoch
    for batch_index, (inputs2, labels2) in enumerate(train_loader):
        test_input =  inputs2.view( inputs2.size(0) , inputs2.size(2)*inputs2.size(3))
### >>> net.eval(...) 
        creloss, accuracy, outputs=net.eval(test_input,labels2,debug)
        print("evaluating",batch_index,creloss,accuracy)

# TODO: End of Training
# make predictions on randomly selected test examples

# >>> net.predict(...) """
for batch_index, (inputs1, labels1) in enumerate(test_loader):     
        tester_input = inputs1.view( inputs1.size(0) , inputs1.size(2)*inputs1.size(3))        
        score, idx=net.predict(tester_input)
        print(score,idx)
