#include<stdio.h>
struct cord
{

	int x  ; int y;

};


int calc_min(int b, int h)

{       struct cord a;
	a.x = b/10;
	a.y  = b%10;


//###############################################################################
//calculates the nearest co ordinate of habitat associated with animal co ordinate
//###############################################################################

	int d[4] ;
	d[1] = h;
	d[0] =  (  (d[1]/10)*10 ) + d[1]%10 -1;
	d[2] = (d[1]/10 +1 )*10  + d[1]%10;
	d[3] =  (d[0]/10 +1 )*10 + d[0]%10;

	int min = 100;
	int temp = 0;
	int temp2 ;
	int marker;
	for(int i = 0 ; i < 4 ;i ++)
	{
		temp = (d[i]/10 - a.x)*( d[i]/10 - a.x) + (d[i]%10 -a.y)*(d[i]%10 -a.y);
		if( temp < min)
	                     {    min=temp; marker=i;       }


	}

	return(d[marker]);


}
