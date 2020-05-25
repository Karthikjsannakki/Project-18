#include<stdio.h>


//###############################################################################
//generates reference b co ordinates and from which rest of the co ordinates can be derived
//###############################################################################

int   lfind  ( int x)

{
	    int temp=0;
            if( x%5 == 0)
		{    temp = ( ( (x-1)/5) *10) + 5; }
	    else
		{ temp  = (x/5) * 10 + x%5 ; }
	   return temp;

} 

