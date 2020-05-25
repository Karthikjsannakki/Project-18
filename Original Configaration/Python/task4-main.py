import argparse
import os
import task2solver
import numpy as np
from task3asolver.task3a import reader 
import xlrd
import sys
import glob
import serial
from datetime import datetime
import time
import parse






####################################################################

'''
initializing arguments

'''

#####################################################################


parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument("arenaimg", help = "Absolute/Relative path of an arena image to be processed.")
parser.add_argument("-s", metavar='\b', help="    Path to save processed image.")
parser.add_argument("-p",metavar='\b',help = 'optional port')
parser.add_argument("--amod",  metavar='\b', help="    Path of the trainned model which is required to identify animals" ,default='rega118.pth')
parser.add_argument("--hmod",  metavar='\b', help="    Path of the trainned model which is required to identitfy habitat",default = 'fullh118.pth')

args = parser.parse_args()

image = os.path.realpath(args.arenaimg)
animalModel = args.amod
habitatModel = args.hmod
port = args.p

####################################################################

'''
function to identify a serial port connected

'''

#####################################################################


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result







####################################################################

'''
getting absolute paths of all file args

'''

#####################################################################



if not (os.path.isfile(image) and os.access(image, os.R_OK) ):
		print("File "+image+" doesn't exist or isn't readable") ; exit()
if not (os.path.isfile(animalModel) and os.access(animalModel, os.R_OK) ):
		print("File "+animalModel+" doesn't exist or isn't readable") ; exit()
if not (os.path.isfile(habitatModel) and os.access(habitatModel, os.R_OK) ):
		print("File "+habitatModel+" doesn't exist or isn't readable") ; exit()
 
savepath = None

if args.s:
	savepath = args.s
	saveDir = os.path.realpath(args.s)
	tempPath = os.path.split(saveDir)[0]
	if not( os.path.isdir(tempPath) and os.access(tempPath, os.W_OK)):
           print("Directory "+tempPath+"  doesn't exist or isn't writable mentioned at 's' flag") ; exit()	




####################################################################

'''
getting all keys of detected images 

'''

#####################################################################




keys = task2solver.countourImage.ImgReader(image ,save_path = savepath )



####################################################################

'''
Image recognition of temporary stored image files

'''

#####################################################################



difj = dict()

for key in keys:
	if key.isnumeric():
		difj[key] = reader('.'+key+'.png',habitatModel,24) ; os.remove('.'+key+'.png')
	else: 
		difj[key] = reader('.'+key+'.png',animalModel,38) ; os.remove('.'+key+'.png')




####################################################################

'''
separating animals and habitats

'''

#####################################################################





dictt = [  (y,i) for (i,y) in difj.items()  ]

anis = [ (i,y) for (i,y) in dictt if not y.isdigit() ] 

habis = [ (i,y) for (i,y) in dictt if  y.isdigit() ] 





####################################################################

'''
loading xlsx file of associativity

'''

#####################################################################



wb = xlrd.open_workbook('a.xlsx')

sheet = wb.sheet_by_index(0)





tyy = list()

for i in range(1,sheet.nrows):
    tyy.append(sheet.cell_value(i,0))


emptyy = dict()



####################################################################

'''
getting all possible associations between different habitat and animals

'''

#####################################################################

for i,j in enumerate(tyy):
    emptyy[j] = [ sheet.cell_value(i+1,t) for t in range(1,sheet.ncols) if  sheet.cell_value(i+1,t)  ]


fin = []
for l,jj in anis:
    for k,ii in habis:
            
            if l in emptyy[k]:
                  
                fin.append( (jj,ii))






from collections import defaultdict 

di = defaultdict(list)
for k,v in fin:
    di[k].append(v)





####################################################################

'''
generating all possible cases for produces associations if multiple association exists

'''

#####################################################################




import itertools


keys = di.keys()
values = (di[key] for key in keys)
combinations = [list(zip(keys, combination)) for combination in itertools.product(*values)]








####################################################################

'''
applying parse module to get numer of node to node traversals and amount of direction changes

'''

#####################################################################











import parse


resource = []
for z,k in enumerate(combinations):
    ld = []
    for o,(i,y) in enumerate(k):
        ld.append(y)
        if o != len(combinations[0])-1:
            ld.append(',')
            ld.append(' ')
    ld.append('\n')    
    for o,(i,y) in enumerate(k):    
        ld.append(i)
        if o != len(combinations[0])-1:    
            ld.append(',')
            ld.append(' ')    
    resource.append((parse.finalizer(''.join(ld)+'#'),z))
    





####################################################################

'''
sorting the results  by minimal traversal and direction changes
'''

#####################################################################




from operator import itemgetter
resource.sort(key=itemgetter(0))


result = resource[0][1]


####################################################################

'''
getting the top most value
'''

#####################################################################




ld = []
for o,(i,y) in enumerate(combinations[result]):
    ld.append(y)
    if o != len(combinations[0])-1:
        ld.append(',')
        ld.append(' ')
ld.append('\n')    
for o,(i,y) in enumerate(combinations[result]):    
    ld.append(i)
    if o != len(combinations[0])-1:    
        ld.append(',')
        ld.append(' ')  



print(''.join(ld))

      

####################################################################

'''
communication serially the list to  the robot

'''

#####################################################################



filepointer = ''.join(ld) + '''#'''

if args.p:
	port = args.p
else : 
	if serial_ports():
		port = serial_ports()[0]



print()
print("first serial port is being considered")
print()
print()




if port:
	ser = serial.Serial(port)
	data = datetime.now()
	print(data.hour,':',data.minute,':',data.second,":",data.microsecond)
	for i in  range(len(filepointer)):
		ser.write(filepointer[i].encode()) ; time.sleep(0.02)
	data  =  datetime.now()
	print(data.hour,':',data.minute,':',data.second,":",data.microsecond)


else:
	print('No ports,use -p to specify explicitly')



