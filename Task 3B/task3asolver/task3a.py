'''
* Team Id : HC#4674
* Author List : Karthik, Anju Thomas, Chesmi 
* Filename : task3a.py
* Theme : Homecoming
* Functions : imageprepare, getnet, habidict, anidict, reader
* Global Variables : None
'''




from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import torch


import warnings
warnings.filterwarnings("ignore")




'''
* Function Name :  imageprepare
* Input : path -> path of an image , x -> number of classes that the model can predict
* Output :  -> image that is transformed to tensor acts as an input to the conv net
* Logic :  scaling, cropping and  normalizing 
* Example Call : imageprepare('1.png',24)
'''




def imageprepare(path,x):
	img = Image.open(path)
	mean =  [0.485, 0.456, 0.406]
	std =  [0.229, 0.224, 0.225]
	size =  transforms.Resize(224)
	crop = transforms.CenterCrop(224)
	
	if x == 38:
		scale = transforms.Scale((118,118))
 
	else :

		scale = transforms.Scale((280,280))


	transform_pipeline = transforms.Compose([scale,size,crop,
                                     	transforms.ToTensor(),
                                        transforms.Normalize(mean,std)])


	img = transform_pipeline(img)
	img = img.unsqueeze(0)
	return(img)








'''
* Function Name : getnet 
* Input : path -> path to the trained model, x-> number of classes
* Output :   a loaded evaluating convnet 
* Logic :  loding convnet from saved state 
* Example Call :  getnet('model.pth,24)
'''




def getnet(path,x):

	
	convnet  = models.resnet18(pretrained=False)
	num_ftrs = convnet.fc.in_features
	convnet.fc = torch.nn.Linear(num_ftrs, x)

	device = "cuda:0" if torch.cuda.is_available() else "cpu"
	if device =='cpu':
		convnet.load_state_dict(torch.load(path,map_location='cpu'))
	else:
		convnet.load_state_dict(torch.load(path))
	return convnet.eval()






'''
* Function Name :  habidict
* Input : x -> as a key of dict
* Output : class name of predicted habitat
* Logic : None
* Example Call :  habidict(22)
'''






def habidict(x):
	labels_of_habitat = { 0:'baseball', 
                   1:'basketball court', 
                   2:'beach', 
                   3:'circular farm',
                   4:'cloud', 
                   5:'commercial area', 
                   6:'dense residential',
                   7: 'desert',
                   8: 'forest', 
                   9:'golf course', 
                   10: 'harbor', 
                   11:'island', 
                   12:'lake', 
                   13:'meadow', 
                   14:'medium residential area', 
                   15:'mountain', 
                   16:'rectangular farm', 
                   17:'river', 
                   18:'sea glacier',
                   19: 'shrubs', 
                   20:'snowberg', 
                   21:'sparse residential area', 
                   22:'thermal power station', 
                   23:'wetland'}

	return( labels_of_habitat[x])





'''
* Function Name :  anidict
* Input : x -> as a key of dict
* Output : class name of predicted animal
* Logic : None
* Example Call :  anidict(22)
'''




def anidict(x):

	labels_of_animals = {0: 'arctic fox', 
			     1: 'bear', 
			     2: 'bee', 
			     3: 'butterfly', 
			     4: 'cat', 
			     5: 'cougar', 
			     6: 'cow', 
			     7: 'coyote', 
			     8: 'crab', 
			     9: 'crocodile', 
			    10: 'deer', 
			    11: 'dog', 
			    12: 'eagle', 
			    13: 'elephant', 
			    14: 'fish', 
			    15: 'frog', 
			    16: 'giraffe', 
     			    17: 'goat', 
		            18: 'hippo', 
			    19: 'horse', 
		            20: 'kangaroo', 
			    21: 'lion', 
		            22: 'monkey', 
		            23: 'otter', 
			    24: 'panda', 
    		            25: 'parrot', 
			    26: 'penguin', 
	  	            27: 'raccoon', 
			    28: 'rat', 
			    29: 'seal', 
			    30: 'shark', 
			    31: 'sheep', 
			    32: 'skunk', 
			    33: 'snake', 
			    34: 'snow leopard', 
			    35: 'tiger', 
			    36: 'yak', 
			    37: 'zebra'}

	return (labels_of_animals[x])





'''
* Function Name :  reader 
* Input : Image -> path of an image, Model-> path of image model,num->number of classes
* Output : classname of habitat or animal according to the class number
* Logic : processing and transforming image, getting predicted number, getting the classname
* Example Call : reader('1.png','model.pth',24)
'''





def reader(Image,Model,num):


	thing=None
	if Image:
		img = imageprepare(Image,num)
		convnet = getnet(Model,num)
		prediction = convnet(img)
		prediction = prediction.data.numpy().argmax()  
		if num == 24:		
			thing = habidict(prediction) 
		elif num == 38:	
			thing = anidict(prediction) 


	return(thing)
