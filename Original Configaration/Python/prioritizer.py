import alphaloc
import locallocator
import distcalc
import netnodecalc
from sys import exit


def prioritize(h,a,s):
	""" returns the list of prioritised list based on near pick and drop recursively
	"""
	seqa = list()
	seqh = list()
	length = len(h)

	sourcemarker = 0 
	marker = 0
	k = 0
	dist = 99
	while(marker <length): 
		for i in range(length):
			
			temp =  distcalc.travel(s, alphaloc.finder(a[i]) )  +  distcalc.travel(alphaloc.finder(a[i]) , netnodecalc.calc_min(a[i], h[i])  )
			
			#print(h[i] not in seqh, a[i] not in seqa)
			if( temp < dist and (h[i] not in seqh or  a[i] not in seqa)):
				dist = temp; k = i 

		
		seqa.append(a[k])
		seqh.append(h[k])
		s   = netnodecalc.calc_min(a[k],h[k])
		marker +=1

		dist = 99 

	return(seqa,seqh)

