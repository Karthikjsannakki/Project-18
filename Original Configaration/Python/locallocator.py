
def calc(i):

	""" returns all four co ordinates associated with an habitat  """
	b=0
	if i%5==0:
		b=  ((i-1)//5,5)
	else:
		b= (i//5,i%5)

	a =(b[0],b[1]-1)
	c = (b[0]+1,b[1])
	d = (a[0]+1,a[1])
	return(a,b,c,d)


