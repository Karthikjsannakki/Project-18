#include <stdio.h>
//#include "distcalc.c"
#include <stdlib.h>

struct vals
{  int a; int b ; int c ; int d ; 
};


struct xxyy {

int x;
int y;


};


//###############################################################################
//returns the next co ordinate after traversing and updates  direction of the robot
//###############################################################################


int  ravel( int l, int h, int *d)
{
    struct xxyy  a,b ;


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


                else {   *d = -90 ; }


                return (a.x-1)*10+a.y;


        }


 else if(vert <0)

        {


                if( *d == 90) { }

                else if( *d == 180) {  *d = 90 ; }

                else if( *d == -90)   {  *d = 90 ; }


                else {   *d = 90 ; }

                return (a.x+1)*10+a.y;


        }

        else if(horz>0)


        {

                if( *d == 180) { }

                else if( *d == 90) {  *d = 180 ; }

                else if( *d == 0)   {  *d = 180 ; }


                else {   *d = 180 ;   }

                return (a.x)*10+a.y-1;


        }

        else


        {


                if( *d == 0) { }

                else if( *d == -90) {  *d = 0 ; }

                else if( *d == 180)   {  *d = 0;  }


                else {   *d = 0 ;   }




                return (a.x)*10+a.y+1;


        }


}









int    adjplease(int b, int a,  int r)


{

struct vals d ;

int o; int t;

d.b = b;
d.a =  (  (d.b/10)*10 ) + d.b%10 -1;
d.c = (d.b/10 +1 )*10  + d.b%10;
d.d =  (d.a/10 +1 )*10 + d.a%10;

int ddir;
int counter1=0;
int counter2=0;
int holder;
int returner;

if( a == d.b)
{
o = distcal(d.a,r);
t = distcal(d.c,r);


if(o<t) { return d.a;} else { return d.c; }

if(o==t) {
        counter1 =0;
	ddir = 180; holder = ddir; returner = d.a;
	
	while( returner != r)
                {

              returner = ravel( returner, r, &ddir);
	      if(holder != ddir) { counter1++;}
	      holder = ddir;

          }

	counter2 =0;
        ddir = 90; holder = ddir; returner = d.c;
        while( returner != r)
                { 

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter2++;}
              holder = ddir;

          }

        if(counter1 < counter2 ) { return d.a ;
				  } 
				else if( counter2> counter1) { return d.c; 
							 } 
	else{   return d.a;  
	    }

return d.a;


}


}
else if( a == d.d)

{

o = distcal(d.a,r);
t = distcal(d.c,r);

if(o<t) { return d.a;} else { return d.c; }


if(o==t) {


        counter1 =0;
        ddir = -90; holder = ddir; returner = d.a;
      
        while( returner != r)
                {

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter1++;}
              holder = ddir;

          }

        counter2 =0;
        ddir = 0; holder = ddir; returner = d.c;
        while( returner != r)
                { 

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter2++;}
              holder = ddir;

          }

        if(counter1 < counter2 ) { return d.a ;
                                  } 
                                else if( counter2> counter1) { return d.c; 
                                                         } 
        else{   return d.a;   
            }











}




}



else if(a == d.c)

{

o = distcal(d.b,r);
t = distcal(d.d,r);

if(o<t) { return d.b;} else { return d.d; }


if(o==t) {


	counter1 =0;
        ddir = -90; holder = ddir; returner = d.b;
       
        while( returner != r)
                {

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter1++;}
              holder = ddir;

          }

        counter2 =0;
        ddir = 180; holder = ddir; returner = d.d;
        while( returner != r)
                { 

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter2++;}
              holder = ddir;

          }

        if(counter1 < counter2 ) { return d.b ;
                                  } 
                                else if( counter2> counter1) { return d.d; 
                                                         } 
        else{   return d.b;  
            }







}


}

else
{

o = distcal(d.b,r);
t = distcal(d.d,r);




if(o<t) {     return d.b;         } else { return d.d; }

if(o==t){


	counter1 =0;
        ddir = 0; holder = ddir; returner = d.b;
    
        while( returner != r)
                {

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter1++;}
              holder = ddir;

          }

        counter2 =0;
        ddir = 90; holder = ddir; returner = d.d;
        while( returner != r)
                { 

              returner = ravel( returner, r, &ddir);
              if(holder != ddir) { counter2++;}
              holder = ddir;

          }

        if(counter1 < counter2 ) { return d.b ;
                                  } 
                                else if( counter2> counter1) { return d.d; 
                                                         } 
        else{   return d.b;   // more ai stuff
            }





}


}




}




