'''
* Team Id : HC#4674
* Author List : Karthik, Anju Thomas, Chesmi 
* Filename : countourImage.py
* Theme : Homecoming
* Functions : AlphaPlacer, NumberPlacer, DetectSubContour, mapper, GrayConverter, ThresholdSubtractor, contourSaver, ContourDrawer, ImageSaver, Imgreader
* Global Variables : stflag, stripper, extension
'''



import os
import numpy as np
import cv2
from task2solver.reference_image_raw_data import image_data as ref_img_data
from task2solver.reference_image_raw_data import pre_defined_locations as pre_defined_locations
import math





def AlphaPlacer(M, area):

	""" Gives the position to place fonts on the image for animals 
	Args:
	M (dict): Contour Momentum
	area (float): Area of contour detected

	"""



	side = math.sqrt(area)
	semi = side / 2
	semi2 =  semi / 4
	cx = int(M['m10']/M['m00'] - semi2)
	cy = int((M['m01']/M['m00']) - semi)
	return cx,cy



def NumberPlacer(M,peri):

	""" Gives the position to place fonts on the image for habitat 
	Args:
	M (dict): Contour Momentum
	peri (float): perimeter of contour detected

	"""

	side = peri / 4
	semi = side / 8
	semi2 = semi / 2
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	return int(cx-semi),int(cy+semi2)



def	DetectSubContour(img, contour_dict, org_cont, cmarkeralpha):

	""" Detects if a animal/Habitat present in a block image segment 
	Args:
	img (ndarray): image matrix
	contour_dict (dict): dictionary with locations as keys and contours as values 
	org_cont (dict): dictionary with locations of habitat as keys and inner contour as values
	cmarkeralpha (dict): dictionary with locations of animals as keys and inner contour as values
	"""


	extractor = list()
	key_list = contour_dict.keys()

	inner_contours = list()

	for i in range(len(org_cont)):
		if i == 0 or (i == 29) or (i < 14*2 and i%2 == 1) or (i > 54 and i%2 == 1 ): 
			continue
		inner_contours.append(org_cont[i])


	essential_inner_contours = dict()

	for i,j in zip(key_list,inner_contours):
		if not i.isnumeric():
			essential_inner_contours[i]=j


	test_keys = essential_inner_contours.keys()



	for key in key_list:

		if key.isnumeric():

			[y,x,w,h] = cv2.boundingRect(contour_dict[key])
			temp  = img[x:x+h,y:y+w]


			aa , ab =   np.copy(temp[0:2,:]), np.copy(temp[:,0:2])
			ac , ad =  np.copy(temp[ temp.shape[0]-2:temp.shape[0]]), np.copy(temp[:,temp.shape[1]-2:temp.shape[1]] )


			temp[0:2,:], temp[:,0:2] =  0,0
			temp[ temp.shape[0]-2:temp.shape[0]] , temp[:,temp.shape[1]-2:temp.shape[1]]  = 0,0
	
	
			temp_gray = GrayConverter(temp)

			ret,thresh = ThresholdSubtractor(temp_gray, 210, 255, 0)


			_,cont,hie = FindContours( thresh)

			temp[ temp.shape[0]-2:temp.shape[0]] , temp[:,temp.shape[1]-2:temp.shape[1]]  = ac,ad
			temp[0:2,:], temp[:,0:2] = aa, ab



			tempvar = np.copy(img[x:x+h,y:y+w])
			


			if  len(cont) > 1: 
				

     				
				font = cv2.FONT_HERSHEY_PLAIN
				
				[y1,x1,w1,h1] = cv2.boundingRect(cont[1])
				if (h1*w1) < 700:
					temp1  =  img[x+11:x+h-10,y+13:y+w-13]
					newdict.append(key)
					#if stflag:
					cv2.imwrite('.'+key+'.png',temp1) 
					cv2.rectangle(img,(y+13,x+11),(y+w-13,x+h-10),(0,0,255),2)
					M = cv2.moments(contour_dict[key])
					x,y = NumberPlacer(M,cv2.arcLength(contour_dict[key],True))

					cv2.putText(img, str(key) ,(x+15,y), font, 3, (0,0,255),3,cv2.LINE_8)




				else :
					temp1  =  temp[x1:x1+h1,y1:y1+w1]
					newdict.append(key)
					#if stflag:
					cv2.imwrite('.'+key+'.png',temp1) 
					cv2.drawContours(temp,cont,1,(0,0,255),2)
					M = cv2.moments(cont[1])
					x,y = NumberPlacer(M,cv2.arcLength(cont[1],True))
					cv2.putText(temp, str(key) ,(x,y), font, 3, (0,0,255),3,cv2.LINE_8)






	for key in test_keys:

		[y,x,w,h] = cv2.boundingRect(essential_inner_contours[key])
		temp  = img[x:x+h,y:y+w]
		
		aa , ab =   np.copy(temp[0:3,:]), np.copy(temp[:,0:3])
		ac , ad =  np.copy(temp[ temp.shape[0]-3:temp.shape[0]]), np.copy(temp[:,temp.shape[1]-3:temp.shape[1]] )

		temp[0:3,:], temp[:,0:3] =  0,0
		temp[ temp.shape[0]-3:temp.shape[0]] , temp[:,temp.shape[1]-3:temp.shape[1]]  = 0,0


		temp_gray = GrayConverter(temp)
		ret,thresh = ThresholdSubtractor(temp_gray, 160, 255, 0)


		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
		thresh = cv2.dilate(thresh, kernel, iterations = 1)


		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
		thresh = cv2.dilate(thresh, kernel, iterations = 1)

		temp[ temp.shape[0]-3:temp.shape[0]] , temp[:,temp.shape[1]-3:temp.shape[1]]  = ac,ad
		temp[0:3,:], temp[:,0:3] = aa, ab


		_,cont,hie = FindContours( thresh)

		if len(cont) > 1: 
			extractor.append(key)

			[y1,x1,w1,h1] = cv2.boundingRect(cmarkeralpha[key])
			cv2.rectangle(img,(y-6,x-6),(y+w+8,x+h+8),(0,0,255),2)
			temp1  =  img[x1:x1+h1,y1:y1+w1]
			newdict.append(key)
			#if stflag:
			cv2.imwrite('.'+key+'.png',temp1) 





	return(extractor, img)




def mapper(img):


	""" Mapper of contours and their locations if habitat or animal exists

	Args:
	img (ndarray): image matrix


	"""

	nparr = np.fromstring(ref_img_data, np.uint8)
	ref_threshold = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	ref_gray = GrayConverter(ref_threshold)

	ret,thresh = ThresholdSubtractor(ref_gray,100,255,0)
	height,width,channel = img.shape
	res = cv2.resize(ref_gray,(width, height), interpolation = cv2.INTER_AREA)
	ret,res = ThresholdSubtractor(res,100,255,0)

	image,contours, hierarchy = FindContours(res)

	new_contour = list()
	contlistforcmark = list()


	for i in range(len(contours)):
		if i == 0 or (i ==  28 or i == 29) or (i < 14*2 and i%2 == 0) or (i > 54 and i%2 == 0 ): 
			continue
		new_contour.append(contours[i])

	for i in range(len(contours)):
		if i < 29 and i>0 and  i%2 ==0 or ((i > 54) and i%2 ==0):# and i%2 == 0) or (i > 54 and i%2 == 0 ): 
			contlistforcmark.append(contours[i])

	cmarkinner = ['F1','E1','D1','C1','B1','A1','F2','A2','F3','A3','F4','A4','F5','A5','F6','E6','D6','C6','B6','A6']

	contour_dict = dict()
	contour_valids = [ i for i in range(len(new_contour)) ]

	for i,j in zip(pre_defined_locations,contour_valids):

		contour_dict[i] = new_contour[j]


	contdictforcmark = dict()
	contour_valids = [ i for i in range(len(contlistforcmark)) ]

	for i,j in zip(cmarkinner,contour_valids):

		contdictforcmark[i] = contlistforcmark[j]

	final_list, img = DetectSubContour(img, contour_dict, contours, contdictforcmark)

	processed_dict = dict()
	for i in final_list:
		processed_dict[i] = contour_dict[i]



	return processed_dict,img


def GrayConverter(image):
	""" Converts an image to a grayscale image

	Args:
		image (ndarray): grayscale matrix

	 """
	gray =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	return(gray)


def ThresholdSubtractor(img, min_value, max_value, mounting_value):
	""" Converts a grayscale image  to binary image "

	Args:
		img (ndarray): 	       grayscale matrix
		min_value (int):       threshold value
		max_value (int):       substituion value for above threshold value
		mounting_value (int):  substituion value for values below threshold

	"""
	ret, thresh = cv2.threshold(img, min_value, max_value, mounting_value)
	return(ret,thresh)


def FindContours(threshold):

	""" Finds contours in a binary image

	Args:
		threshold (ndarray): binary image

	"""
	image, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return(image, contours, hierarchy)


def  contourSaver(key, img):
	
	""" saves the contour segment with the name key 

	Args:
		key (str): filename to be saved
		img (ndarray): contour image matrix
	"""

	cv2.imwrite(os.path.join(stripper,key+extension),img)


def ContourDrawer(image, contour_dict):

	""" Draws contours in a binary image

	Args:
		image (ndarray):  image matrix
		contour_dict (dict):  dictionary of contour locations and contour list detected
		
	"""
	font = cv2.FONT_HERSHEY_PLAIN



	empty = list()
	for i in contour_dict.keys():
		empty.append( contour_dict[i])




	for i,j in zip(range(len(empty)), contour_dict.keys()):

		M = cv2.moments(empty[i])

		if j.isnumeric(): x,y = NumberPlacer(M,cv2.arcLength(empty[i],True))
		else : x,y = AlphaPlacer(M,cv2.contourArea(empty[i]))


		cv2.putText(image, str(j) ,(x,y), font, 2.4,(0,0,255),3,cv2.LINE_8)

	return(image)


def ImageSaver(image, savePath):

	""" saves the processed image in savePath directory

	Args:
		image (ndarray): processed image matrix
		savePath (str):  path to be saved
		
	"""
	
	cv2.imwrite(savePath,image)


def ImgReader(imagePath,  save_path = None, stripper_path = None):
	"""
	The main entry of the module which reads an image from imagePath
	saves the processed image if save_path is given as well as
	saves anima/habitat segments  in stripper_path

	Args:
		imagePath (str): path to the image
		savePath(str): path to which the processed image to be saved
		stripper_path(str): path to which the contour segments to be saved
	"""

	global stripper
	global stflag
	global newdict
	newdict = list()
	stflag =True if stripper_path else False

	imagePath = os.path.realpath(imagePath)

	
	



	stripper = None
	if (save_path ):  saver = save_path; save_path = os.path.realpath(save_path);

	if (stripper_path ): stripper = stripper_path; stripper = os.path.realpath(stripper); 

	origdir, contFile = os.path.split(imagePath)

	global extension
	wantedFile , extension = os.path.splitext(contFile)

	if stripper:
		if 	os.path.isdir(os.path.join(stripper,wantedFile)):
			__import__("shutil").rmtree(os.path.join(stripper,wantedFile))

		os.mkdir(os.path.join(stripper,wantedFile))
		stripper = os.path.join(stripper,wantedFile)

	img = cv2.imread(imagePath)

	mapped_dict,anotherImg = mapper(img)


	processed_image = ContourDrawer(anotherImg, mapped_dict)
	
	if save_path:
		ImageSaver(processed_image, saver)
	return newdict

if __name__ == "__main__":
	pass

