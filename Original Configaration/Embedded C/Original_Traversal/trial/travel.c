#include<stdio.h>


struct xy {

	int x;
	int y;


};


int travell(int l, int h, int *d);

//###############################################################################
//calls a single motion function updates direction and returns the next co ordinate
//###############################################################################




int  travell( int l, int h, int *d)
{
	struct xy  a,b ;


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
                     
	if( *d == -90) {    forward_cus(); }

else if( *d == 180) {  *d = -90 ; lr_cus(180); }

		else if( *d == 90)   {  *d = -90 ;lr_cus(-90); }


		else {   *d = -90 ; lr_cus(0);   }


		return (a.x-1)*10+a.y;   


	}


	else if(vert <0)

	{
                 

                if( *d == 90) { forward_cus();	  }

                else if( *d == 180) {  *d = 90 ; lr_cus(0); }

                else if( *d == -90)   {  *d = 90 ;   lr_cus(-90); }


                else {   *d = 90 ; lr_cus(180);   }

		return (a.x+1)*10+a.y; 


	}




	else if(horz>0)


	{   

                if( *d == 180) {     forward_cus();  }

                else if( *d == 90) {  *d = 180 ;lr_cus(180); }

                else if( *d == 0)   {  *d = 180 ; lr_cus(-90); }


                else {   *d = 180 ; lr_cus(0);   }

		return (a.x)*10+a.y-1;   


	}



	else


	{
              

                if( *d == 0) { forward_cus(); }

                else if( *d == -90) {  *d = 0 ; lr_cus(180); }

                else if( *d == 180)   {  *d = 0 ; lr_cus(-90); }


                else {   *d = 0 ;    lr_cus(0);   }




		return (a.x)*10+a.y+1;


	}





}
