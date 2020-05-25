#include<stdio.h>


//###############################################################################
//returns the direction of animals block with respect to the eyantra logo as north and which is at 90 degrees to our reference
//###############################################################################

struct some
{

	int x ; int y;

};



//------------------------------------------


int director( int val  )
{


	struct some v ;


	v.x = val/10   ;
	v.y = val % 10 ;



	if( v.x == 0  )
	{

	if(v.y == 0) { return 225  ; }

else if(v.y == 5) { return  -45 ;  }

  else  if (v.y  )  { return(-90) ; }




}


else if(    v.x == 5     )


{
  if(v.y == 0) { return    135; }

  else if(v.y == 5) { return   45 ;  }

  else  return(90) ; 




}



  else if( v.x > 0 && v.x < 5  && v.y ==5 )   { return 0; }


else if( v.x > 0 && v.x  < 5  && v.y == 0 )   { return 180; }






}
  
