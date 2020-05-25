
'''
* Team Id : HC#4674
* Author List : Karthik, Anju Thomas, Chesmi 
* Filename : main.py
* Theme : Homecoming
* Functions : None
* Global Variables : None
'''







import argparse
import os
import task2solver
from task3asolver.task3a import reader 

# creating a parser for arguments
parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)



#adding flags (arenaimage,-s,--amod,--hmod)
parser.add_argument("arenaimg", help = "Absolute/Relative path of an arena image to be processed.")
parser.add_argument("-s", metavar='\b', help="    Path to save processed image.")
parser.add_argument("--amod",  metavar='\b', help="    Path of the trainned model which is required to identify animals" ,default='rega118.pth')
parser.add_argument("--hmod",  metavar='\b', help="    Path of the trainned model which is required to identitfy habitat",default = 'fullh118.pth')

args = parser.parse_args()

image = os.path.realpath(args.arenaimg)
animalModel = args.amod
habitatModel = args.hmod



#verifying args required to process arena image is valid and reachable
if not (os.path.isfile(image) and os.access(image, os.R_OK) ):
		print("File "+image+" doesn't exist or isn't readable") ; exit()
if not (os.path.isfile(animalModel) and os.access(animalModel, os.R_OK) ):
		print("File "+animalModel+" doesn't exist or isn't readable") ; exit()
if not (os.path.isfile(habitatModel) and os.access(habitatModel, os.R_OK) ):
		print("File "+habitatModel+" doesn't exist or isn't readable") ; exit()
 
savepath = None


#veryfying the savepath is writable
if args.s:
	savepath = args.s
	saveDir = os.path.realpath(args.s)
	tempPath = os.path.split(saveDir)[0]
	if not( os.path.isdir(tempPath) and os.access(tempPath, os.W_OK)):
           print("Directory "+tempPath+"  doesn't exist or isn't writable mentioned at 's' flag") ; exit()	






#getting keys from task2solver module 
keys = task2solver.countourImage.ImgReader(image ,save_path = savepath )

#initializing dict to print on terminal
dictprocessed = dict()



#processing temporary saved contours of arenaimage
for key in keys:

	if key.isnumeric():
		dictprocessed[key] = reader('.'+key+'.png',habitatModel,24) ; os.remove('.'+key+'.png')
	else: 
		dictprocessed[key] = reader('.'+key+'.png',animalModel,38) ; os.remove('.'+key+'.png')

print(dictprocessed)




