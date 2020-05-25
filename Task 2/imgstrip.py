'''
* Team Id : HC#4674
* Author List : Karthik, Anju Thomas, Chesmi 
* Filename : imgstrip.py
* Theme : Homecoming
* Functions : None
* Global Variables : None
'''


import argparse
import os
import task2solver

parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)


parser.add_argument("imgpath", help = "Absolute/Relative path of an image to be processed.")
parser.add_argument("-s", "--save", metavar='\b', help="    Path to save processed image.")
parser.add_argument("-c", "--cc", metavar='\b', help="    Path of directory to save stripped images.")

args = parser.parse_args()



imagePath = args.imgpath
saveDir = args.save
conDir = args.cc






if imagePath:
    imagePath = os.path.realpath(imagePath)
    if not (os.path.isfile(imagePath) and os.access(imagePath, os.R_OK) ):
           print("File "+imagePath+" doesn't exist or isn't readable") ; exit()   

if saveDir: 
    saveDir = os.path.realpath(saveDir)
    tempPath = os.path.split(saveDir)[0]
    if not( os.path.isdir(tempPath) and os.access(tempPath, os.W_OK)):
           print("Directory "+tempPath+"  doesn't exist or isn't writable mentioned at 'save/s' flag") ; exit()  

if conDir:
    conDir = os.path.realpath(conDir)
    if not( os.path.isdir(conDir) and os.access(conDir, os.W_OK)):
           print("Directory "+conDir+"  doesn't exist or isn't writable  mentioned as 'c/cc' flag") ; exit()               



task2solver.countourImage.ImgReader(imagePath, saveDir, conDir )
