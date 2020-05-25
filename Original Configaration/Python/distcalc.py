

def travel(a,b):

	""" return the total node to node traversal of a pick and drop sequence
	"""
	d = 0


	while a != b:
		 
		vert = a[0] - b[0]
		horz = a[1] - b[1]
		
		if vert > 0:
			a=(a[0]-1,a[1]) ; d+=1 ;
		elif vert <0:
			a = (a[0]+1,a[1]) ; d+=1;
		elif horz >0:
			a = (a[0],a[1]-1) ; d+=1 ;
		else :
			a = (a[0],a[1]+1) ; d+=1 ;
	return(d)



 
