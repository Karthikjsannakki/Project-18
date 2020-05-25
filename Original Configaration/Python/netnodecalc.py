
def finder(a):
	return((int(a[1])-1, ord(a[0])-ord('A')))



def calc(i):
        if i%5 ==0:
                b = ((i-1)//5,5)
        else :
                b = (i//5,i%5)

        min = 0
        a =(b[0],b[1]-1) 
        c = (b[0]+1,b[1]) 
        d = (a[0]+1,a[1])



def calc_min(g,i):

	""" returns a node of an habitat thats is near to animal associated with """
	g = finder(g)
	if i%5 ==0:
		b = ((i-1)//5,5)
	else :
		b = (i//5,i%5)

	min = 100 ; marker = 0
	a =(b[0],b[1]-1)
	c = (b[0]+1,b[1])
	d = (a[0]+1,a[1])
	for x in [b,a,d,c]:
		temp = (x[0]-g[0])**2 + (x[1]-g[1])**2

		if temp < min:
			min = temp
			marker = x
	return(marker)





