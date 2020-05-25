
import alphaloc
import locallocator
import traversal
import distcalc
import netnodecalc
import argparse
import prioritizer





def finalizer(file):

        """ returns a number node to node traversals and change in directions for a complete traversal of given list passed"""
        habis = list()
        i=0
        while(file[i] != '\n'):
            if( file[i] != ','):
                if( file[i].isdigit()) :
                    temp = int( file[i])
                    if( file[i+1].isdigit()):
                        temp = temp *10 + int(file[i+1]) ; i +=1 

                    habis.append(temp)
            i+=1




        animals = list()
        i=0 
        while( file[i] != '#'):
            if( file[i].isalpha()):
                st = file[i]+file[i+1];

                i +=2 
                animals.append(st)
            else:
                i+=1



        animals,habis = prioritizer.prioritize(habis,animals,(0,0))


        travel_list = list()
        for i in range(len(animals)):
            travel_list.append(animals[i]);travel_list.append(habis[i])



        last = len(travel_list)

        destination = netnodecalc.calc_min(travel_list[last-2],travel_list[last-1])



        nodes = list()

        for i in range(len(travel_list)):
            if ( not  str(travel_list[i]).isdigit()):
                nodes.append( alphaloc.finder(travel_list[i]) )
            else:
                nodes.append( netnodecalc.calc_min( travel_list[i-1], travel_list[i]))



        s = (0,0)


        dir = 90
        tt= 0
        count = 0 
        turns = 0


        for i in range(last):


            d = nodes[i]
            while(s  != d):
                (s,dir,count,turns)  = traversal.travel(s,d,dir,count,turns)

        return(count,turns)


