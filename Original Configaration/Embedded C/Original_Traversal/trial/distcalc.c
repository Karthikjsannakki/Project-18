#include<stdio.h>

struct co_ord {

	int x; int y ;


};

//###############################################################################
//calculates the node traversal done for a both pick and drop from current location of the robot
//###############################################################################


int distcal(int c, int d)

{      struct co_ord a,b;

	a.x = c/10 ; a.y = c%10;
	b.x = d/10 ; b.y = d%10;

	



	int vert = 0;
	int horz = 0;
	int k = 0;
	while( ! (a.x == b.x && a.y == b.y) )
	{	
		vert = a.x  - b.x;
		horz  = a.y  - b.y;
		
		if (vert > 0 )
	{ a.x = a.x -1  ; k++;  }


		else if( vert < 0)
	{  a.x = a.x +1 ;  k++;      }

		else if( horz > 0)
	{   a.y  =  a.y -1  ; k++;     }

		else
	{   a.y = a.y +1 ;k++;    }
	}
	return k;

}

