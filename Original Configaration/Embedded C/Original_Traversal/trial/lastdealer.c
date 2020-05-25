#include<stdio.h>
//#include "locallocator.c"

struct last_co {

	int a;
	int b;
	int c;
	int d;



};





struct lasss {

	int x ; int y;

};



//###############################################################################
//performs drop sequences based on current node of habitat and reference node of habitat which is b co ordinate
//###############################################################################

void deallast(int x, int z,int *d)
{

	struct lasss l ;

	
	l.x  =    x/10;
	l.y   =   x%10;
	
	struct  last_co dd;
	
	
	dd.b = z;
	dd.a =  (  (dd.b/10)*10 ) + dd.b%10 -1;
	dd.c = (dd.b/10 +1 )*10  + dd.b%10;
	dd.d =  (dd.a/10 +1 )*10 + dd.a%10;






	if(   l.x > 0  && l.x < 5 && l.y > 0 && l.y < 5    )

	{
		if ( x == dd.b )

		{
		if( *d == 180 ) { forward_half(); right_drop_seq(); }

	else if( *d == 90) { forward_half(); left_drop_seq(); }
	


else {    }


	             }

		      else if( x == dd.c) 
		  			
			{          		


                       if( *d == -90 ) { forward_half();     right_drop_seq(); }

  			else if( *d == 180) { forward_half();          left_drop_seq(); }
 


			else {    }




		      }





		else if( x == dd.a) 
		      {
						


                       if( *d == 90 ) { forward_half(); right_drop_seq(); }

  			else if( *d == 0) { forward_half(); left_drop_seq(); }
 


			else {    }




		      }



		else if( x == dd.d) 
			{  
						


                       if( *d == 0 ) { forward_half() ; right_drop_seq(); }

  			else if( *d == -90) { forward_half(); left_drop_seq(); }
 


			else {    }




			 }


                       else {}





   }


 	     
	

	else if( (l.x == 0 || l.x == 5) ||  ( l.y == 0 || l.y == 5) )                    

{

    
       if( l.x == 0) 
	{ 

               if (l.y !=0 && l.y !=5)  
   
                 {                         

                      if( x == dd.b)  {        

				if(*d == 180)  {             forward_half() ; right_drop_seq();  }

                                      }
	       

	       }




       }
 
    else if( l.x == 5) 
	{ 

               if (l.y !=0 && l.y !=5)  
   
                {                         

                      if( x == dd.b)  
				{        

				if( *d == 0)  {              forward_half() ; right_drop_seq();  }

                                }
	       

	       }




                


        }





else {}



}

}




