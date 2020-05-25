# import required libraries
from PIL import Image
import csv
from torchvision import transforms
import pandas as pd
import numpy as np
from torch.utils.data.dataset import Dataset
from random import randint 
import os
import math

def create_meta_csv(dataset_path, destination_path):
    """Create a meta csv file given a dataset folder path of images.

    This function creates and saves a meta csv file named 'dataset_attr.csv' given a dataset folder path of images.
    The file will contain images and their labels. This file can be then used to make
    train, test and val splits, randomize them and load few of them (a mini-batch) in memory
    as required. The file is saved in dataset_path folder if destination_path is not provided.

    The purpose behind creating this file is to allow loading of images on demand as required. Only those images required are loaded randomly but on demand using their paths.
    
    Args:
        dataset_path (str): Path to dataset folder
        destination_path (str): Destination to store meta file if None provided, it'll store file in dataset_path

    Returns:
        True (bool): Returns True if 'dataset_attr.csv' was created successfully else returns an exception
    """


    previos = os.getcwd()
    if destination_path == None:
            destination_path = dataset_path
    else:
        previos = os.getcwd()
        os.chdir(destination_path)
        destination_path = os.getcwd()
        os.chdir(previos)



    print(destination_path)
    # Change dataset path accordingly
    os.chdir(dataset_path)

    DATASET_PATH = os.getcwd()

    if  os.path.exists(os.path.join(destination_path, "dataset_attr.csv")):
       os.remove(os.path.join(destination_path, "dataset_attr.csv")) 
    if not os.path.exists(os.path.join(destination_path, "dataset_attr.csv")):
        
        with open(os.path.join(destination_path, "dataset_attr.csv"),'a') as file:
            write = csv.writer(file)

            write.writerow(['path','label'])
        # Make a csv with full file path and labels
        
        for folder in os.listdir(DATASET_PATH):
           
            if os.path.isdir(os.path.join(DATASET_PATH,folder)):
                
                new_path = os.path.join(DATASET_PATH,folder)
                
                for img in os.listdir(new_path):
                    
                    img_list = []
                    
                    if img.endswith('.jpg'):
                        
                        image = os.path.join(new_path,img)
                        
                        value = folder 

                        img_list.append(image)
                        img_list.append(value)
                        with open(os.path.join(destination_path, "dataset_attr.csv"),'a') as file:
                            write = csv.writer(file)
                            write.writerow(img_list)
        # change destination_path to DATASET_PATH if destination_path is None 
        

        # write out as dataset_attr.csv in destination_path directory

        # if no error
        os.chdir(previos)
        return True



def create_and_load_meta_csv_df(dataset_path, destination_path, randomize=True, split=None):
    """Create a meta csv file given a dataset folder path of images and loads it as a pandas dataframe.

    This function creates and saves a meta csv file named 'dataset_attr.csv' given a dataset folder path of images.
    The file will contain images and their labels. This file can be then used to make
    train, test and val splits, randomize them and load few of them (a mini-batch) in memory
    as required. The file is saved in dataset_path folder if destination_path is not provided.

    The function will return pandas dataframes for the csv and also train and test splits if you specify a 
    fraction in split parameter.
    
    Args:
        dataset_path (str): Path to dataset folder
        destination_path (str): Destination to store meta csv file
        randomize (bool, optional): Randomize the csv records. Defaults to True
        split (double, optional): Percentage of train records. Defaults to None

    Returns:
        dframe (pandas.Dataframe): Returns a single Dataframe for csv if split is none, else returns more two Dataframes for train and test splits.
        train_set (pandas.Dataframe): Returns a Dataframe of length (split) * len(dframe)
        test_set (pandas.Dataframe): Returns a Dataframe of length (1 - split) * len(dframe)
        
        
    
    """
    
    if create_meta_csv(dataset_path, destination_path=destination_path):   
        
        if destination_path == None:
            destination_path = dataset_path
        else:
            previos = os.getcwd()
            os.chdir(destination_path)
            destination_path = os.getcwd()
            os.chdir(previos)        
        
        
        dframe = pd.read_csv(os.path.join(destination_path, 'dataset_attr.csv'))

    # shuffle if randomize is True or if split specified and randomize is not specified 
    
        if randomize == True or (split != None and randomize == None):
        
            dframe.sample(frac=1)
    
    


        if split != None:
           train_set, test_set = train_test_split(dframe, split)
         
        return dframe, train_set, test_set


def train_test_split(dframe, split_ratio):
    """Splits the dataframe into train and test subset dataframes.

    Args:
        split_ration (float): Divides dframe into two splits.
    Returns: 
        
        train_data (pandas.Dataframe): Returns a Dataframe of length (split_ratio) * len(dframe)
        test_data (pandas.Dataframe): Returns a Dataframe of length (1 - split_ratio) * len(dframe)
    """
    # divide into train and test dataframe
    
    
    x = int(split_ratio*len(dframe))
    
    train_data = dframe[0:x]
    
    y = len(dframe[:]) - x
   
    test_data = dframe[y:len(dframe)]
    
    return train_data, test_data

class ImageDataset(Dataset):
    """Image Dataset that works with images
    
    This class inherits from torch.utils.data.Dataset and will be used inside torch.utils.data.DataLoader
    Args:
        data (str): Dataframe with path and label of images.
        transform (torchvision.transforms.Compose, optional): Transform to be applied on a sample. Defaults to None.
    
    Examples:
        >>> df, train_df, test_df = create_and_load_meta_csv_df(dataset_path, destination_path, randomize=randomize, split=0.99)
        >>> train_dataset = dataset.ImageDataset(train_df)
        >>> test_dataset = dataset.ImageDataset(test_df, transform=...)
    """

    def __init__(self, data, transform=None):
        self.data = data
        self.transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])])
        self.classes =  len(data['label'].unique())

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        
        
        img_path = self.data.iloc[idx]['path']
        image =   Image.open(img_path) 
        yin = img_path[::-1]
        needed = []

        for i in yin:
                if i != '/' : needed.append[i]  
                if  i == '/':  break;    
        string = ''
        for i in  needed:
            string += i                  
        label =    self.classes                   # get label (derived from self.classes; type: int/long) of image
        
        if self.transform:
            image = self.transform(image)

        return image, label


if __name__ == "__main__":
    # test config
    dataset_path = '../Data/fruits'
    dest = '../Data/fruits'
    classes = 5
    total_rows = 4323
    randomize = True
    clear = True
    
    # test_create_meta_csv()
    df, trn_df, tst_df = create_and_load_meta_csv_df(dataset_path, destination_path=dest, randomize=randomize, split=0.99)
    print(df.describe())
    print(trn_df.describe())
    print(tst_df.describe())
