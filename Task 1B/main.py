
# Homecoming (eYRC-2018): Task 1B
# Fruit Classification with a CNN
import torchvision
from model import FNet
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import os
from util import dataset
# import required modules

def train_model(dataset_path, debug=False, destination_path='', save=False):
    """Trains model with set hyper-parameters and provide an option to save the model.

	This function should contain necessary logic to load fruits dataset and train a CNN model on it. It should accept dataset_path which will be path to the dataset directory. You should also specify an option to save the trained model with all parameters. If debug option is specified, it'll print loss and accuracy for all iterations. Returns loss and accuracy for both train and validation sets.

	Args:
		dataset_path (str): Path to the dataset folder. For example, '../Data/fruits/'.
		debug (bool, optional): Prints train, validation loss and accuracy for every iteration. Defaults to False.
		destination_path (str, optional): Destination to save the model file. Defaults to ''.
		save (bool, optional): Saves model if True. Defaults to False.

	Returns:
		loss (torch.tensor): Train loss and validation loss.
		accuracy (torch.tensor): Train accuracy and validation accuracy.
    """

	# Write your code here
	# The code must follow a similar structure
	# NOTE: Make sure you use torch.device() to use GPU if available
    

    
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    
    
    #hyper paramaeteers
    num_epochs = 5
    num_classes = 5
    batch_size = 4
    learning_rate = 0.001
    
    df, df_train, df_test = dataset.create_and_load_meta_csv_df(dataset_path='../Data/fruits/', dest='../Data/fruits/', randomize=True, split=0.8)
    
    
    train_loader = torch.utils.data.DataLoader(dataset=df_train,
                                           batch_size=batch_size, shuffle=True)
    
    
    
    
    test_loader = torch.utils.data.DataLoader(dataset=df_test,
                                           batch_size=batch_size, shuffle=True)
        
    
    total_step = len(train_loader)
    
    model = FNet( num_classes).to(device)
    
    criterion = nn.CrossEntropyLoss()
    
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    
    
    
    
    if debug == True:
        for epoch in range(num_epochs):
          for i, (images, labels) in enumerate(train_loader):
              images = images.to(device)
              labels = labels.to(device)
        
        # Forward pass
              outputs = model(images)
              loss = criterion(outputs, labels)
          
        # Backward and optimize
              optimizer.zero_grad()
              loss.backward()
              optimizer.step()
          
              if (i+1) % 5 == 0 and debug == True:
                      print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
                  
    
    
    
    if destination_path == '':
        
        torch.save(model.state_dict(), 'model.ckpt')
    
    else:
              
          DATASET_PATH = os.path.abspath(dataset_path)
          torch.save(model.state_dict(), os.path.join(DATASET_PATH, "/model.ckpt"))


if __name__ == "__main__":
	train_model('../Data/fruits/', save=True, destination_path='./')
