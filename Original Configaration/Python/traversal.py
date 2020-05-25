
def travel(a,b,d,count,turn):

	"""returns destination co ordinate value and direction and updates of turns and change in direction from node to node traversal
	"""
	vert = a[0] - b[0]
	horz = a[1] - b[1]
	if vert > 0:

		if d != -90:
			turn += 1

		if(d == -90):
			d = -90
		elif (d == 180):
			d = -90
		elif (d == 90):
			d = -90

		else :
			d = -90


		count += 1

		a = (a[0]-1,a[1])
		return(a,d,count,turn)

	elif vert <0:

		if d != 90:
			turn += 1
		if(d == 90):
			d = 90
		elif (d == 180):
			d = 90
		elif (d == -90):
			d = 90
		else :
			d = 90


		count += 1
		return(((a[0]+1,a[1]),d,count,turn))
	elif horz >0:
		
		if d != 180:
			turn += 1
		if(d == 180):
			d = 180
		elif (d == 90):
			d = 180
		elif (d == 0):
			d = 180
		else :
			d = 180


		count += 1
		return(((a[0],a[1]-1),d,count,turn))



	else :
		if d != 0:
			turn += 1

		if(d == 0):
			d = 0
		elif (d == -90):
			d = 0
		elif (d == 180):
			d = 0

		else :
			d = 0

		count += 1



		return(((a[0],a[1]+1),d,count,turn))

