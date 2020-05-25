'''
* Team Id : HC#4674
* Author List : Karthik, Anju Thomas, Chesmi 
* Filename : main.py
* Theme : Homecoming
* Functions : None
* Global Variables : None
'''







import task3asolver 
import argparse
import os


# creating a parser for arguments
parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter,add_help = False)



#adding flags (-a,-h,--amod,--hmod)
parser.add_argument("-a", help = "Absolute/Relative path of an animal image to be identified.")
parser.add_argument("-h", help = "Absolute/Relative path of a habitat image to be identified.")
parser.add_argument("--amod",  metavar='\b', help="    Path of the trainned model which is required to identify animals" ,default='rega118.pth')
parser.add_argument("--hmod",  metavar='\b', help="    Path of the trainned model which is required to identitfy habitat",default = 'fullh118.pth')

args = parser.parse_args()


animalImage = animalModel = habitatImage = habitatModel = None
habitat = animal = None



#verifying args required to classify animal is valid and reachable
if args.a:
	animalImage = args.a
	animalModel = args.amod
	animalImage = os.path.realpath(animalImage)
	animalModel = os.path.realpath(animalModel)

	if not (os.path.isfile(animalImage) and os.access(animalImage, os.R_OK) ):
		print("File "+animalImage+" doesn't exist or isn't readable") ; exit() 
	if not (os.path.isfile(animalModel) and os.access(animalModel, os.R_OK) ):
		print("File "+animalModel+" doesn't exist or isn't readable") ; exit() 
	animal =  task3asolver.task3a.reader(animalImage, animalModel, 38)







#verifying args required to classify habitat is valid and reachable
if args.h:
	habitatImage = args.h
	habitatModel = args.hmod
	habitatImage = os.path.realpath(habitatImage)
	habitatModel = os.path.realpath(habitatModel)



	if not (os.path.isfile(habitatImage) and os.access(habitatImage, os.R_OK) ):
		print("File "+habitatImage+" doesn't exist or isn't readable") ; exit() 
	if not (os.path.isfile(habitatModel) and os.access(habitatModel, os.R_OK) ):
		print("File "+habitatModel+" doesn't exist or isn't readable") ; exit() 
 
	habitat = task3asolver.task3a.reader(habitatImage,  habitatModel, 24)


#printing the appropriate output
if not ( habitatImage or animalImage): print('None args specified')
if habitatImage :
	print("habitat is",habitat)
if animalImage :
	print("animal is", animal)


