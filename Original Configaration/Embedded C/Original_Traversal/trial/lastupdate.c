#include<stdio.h>


struct yx {

	int x;
	int y;


};



//###############################################################################
//updates the direction and co ordinate while dropping the block
//###############################################################################


int  lup( int l, int h, int *d)
{
	struct yx  a,b ;


	a.x =  l/10;
	a.y  = l%10 ;

	b.x = h/10;
	b.y = h%10;

	int vert ;
	int horz ;

	vert = a.x - b.x;
	horz = a.y - b.y;



	if(vert> 0)

	{

	     if( *d == -90) { }

         else if( *d == 180) {  *d = -90 ; }

		else if( *d == 90)   {  *d = -90 ; }


		else {   *d = -90 ;   }


		return (a.x-1)*10+a.y;


	}


	else if(vert <0)

	{


                if( *d == 90) {  }

                else if( *d == 180) {  *d = 90 ;  }

                else if( *d == -90)   {  *d = 90 ; }


                else {   *d = 90 ; }

		return (a.x+1)*10+a.y;


	}




	else if(horz>0)


	{

                if( *d == 180) {  }

                else if( *d == 90) {  *d = 180 ; }

                else if( *d == 0)   {  *d = 180 ;  }


                else {   *d = 180 ;  }

		return (a.x)*10+a.y-1;


	}



	else


	{


                if( *d == 0) {  }

                else if( *d == -90) {  *d = 0 ; }

                else if( *d == 180)   {  *d = 0 ;  }


                else {   *d = 0 ; }




		return (a.x)*10+a.y+1;


	}





}
