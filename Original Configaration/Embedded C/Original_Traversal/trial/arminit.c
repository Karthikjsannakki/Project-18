#include<stdio.h>

//#include "dirani.c"



void resol( int a, int *d )
{


//###############################################################################
// performs arm pick up sequences based on direction of the robot and the direction of associated animal to the arena
//###############################################################################


	int gd = director(a);

	if ( gd == -90)

	{
	              if( *d   == -90) {         front_seq();                   }
	
	
              else if(*d == 180) {       left_pick_seq();                           }

        	 else if(*d ==  0)   {      right_pick_seq();                       }

		else { }


	}



else if ( gd == 0)

	{


           if( *d   == 0) {    front_seq();         }

  
          else if(*d == -90) {        left_pick_seq();         }

            else if(*d == 90)   {     right_pick_seq();           }
           else {} 

	}


else if ( gd == 90)

{

           if( *d   == 90) {    front_seq();       }

  
          else if(*d == 180) {   right_pick_seq();             }

          else if(*d == 0)   {         left_pick_seq();         }

           else {} 
  
}

else if ( gd == 180)

{

           if( *d   == 180) {    front_seq();           }

  
          else if(*d == 90) {      left_pick_seq();            }

         else if(*d == -90)   {       right_pick_seq();                        }
  	  else {} 


}




else if( gd == 135) {

	if(*d == 90) { slight_left_seq(); }

	else if( *d == 180) {  slight_right_seq();}

	 else {} 

}
 



else if(gd == 45) {

		if(*d == 0) { slight_left_seq(); }

		else if( *d ==90) { slight_right_seq(); }
 		else {}


}

else if (gd == -45) {

		if(*d == 0) {   slight_right_seq();  }

		else if( *d == -90) { slight_left_seq(); }
	
		else {} 


}

else {

    if(a ==0) {      if(*d == 90)   {  slight_down_left_seq();  } 
                               
                     




            }





}
 



}





