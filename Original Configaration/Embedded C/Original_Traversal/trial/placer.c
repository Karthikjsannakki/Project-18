

#include <stdio.h>

struct placer_co {

	int a;
	int b;
	int c;
	int d;
};

//###############################################################################
//animal blocks drop sequence based on current node and reference co ordinate and direction of the robot
//###############################################################################

void placeit(int a, int d, int ref, int *dir) {

	struct placer_co dd;

	dd.b = ref;
	dd.a = ((dd.b / 10) * 10) + dd.b % 10 - 1;
	dd.c = (dd.b / 10 + 1) * 10 + dd.b % 10;
	dd.d = (dd.a / 10 + 1) * 10 + dd.a % 10;

	if (a == dd.b)

	{

		if (d == dd.a) {

			if (*dir == 180)

			{
				velocity(246,255);   forward_half();   right_drop_seq();  forwarder();   
			}

			else if (*dir == 90)
			{
			
				 make_correct_direction(180); velocity(246,255);  forward_half();  right_drop_seq();   forwarder();
			}

		}


		else if (d == dd.c)
		{


			if (*dir == 180)
			{
				 make_correct_direction(0); velocity(246,255);  forward_half();  left_drop_seq();   forwarder();
			}

			else if (*dir == 90)
			{
				 forward_half();  left_drop_seq();  forwarder();
				 
			}

		}

	}
	


	else if (a == dd.c)

	{

		if (d == dd.b) {

			if (*dir == -90)

			{
				velocity(246,255);   forward_half();   right_drop_seq();  forwarder();   
			}

			else if (*dir == 180)

			{
				make_correct_direction(180); velocity(246,255);  forward_half();  right_drop_seq();   forwarder();
			}

		}

		else if (d == dd.d) {

			if (*dir == 180)

			{
				 forward_half();  left_drop_seq();  forwarder();
			}

			else if (*dir == -90) {
				 make_correct_direction(0); velocity(246,255);  forward_half();  left_drop_seq();   forwarder();
			}
			

		}

	}

	else if (a == dd.d)

	{

		if (d == dd.a) {
			
			if (*dir == -90)

		 {              forward_half();  left_drop_seq();  forwarder();                  }

			else  if (*dir == 0)

		{                make_correct_direction(0); velocity(246,255);  forward_half();  left_drop_seq();   forwarder();              }




		}

		else if (d == dd.c)


		{

			if (*dir == -90)
		{  make_correct_direction(180); velocity(246,255);  forward_half();  right_drop_seq();   forwarder();         }


			
			else if (*dir == 0)
		{  velocity(246,255);   forward_half();   right_drop_seq();  forwarder();              }



		}

	}

	else

	{    
		

        if (d == dd.b) {


			if (*dir == 0) {  forward_half();  left_drop_seq();  forwarder();                   }
			

			else if (*dir == 90)
		{            make_correct_direction(0); velocity(246,255);  forward_half();  right_drop_seq();   forwarder();              }



		}

              else    if (d == dd.d) {
	                  
					  
	                  
	                  if (*dir == 90)
                  {                   velocity(246,255);   forward_half();   right_drop_seq();  forwarder();                }


	                  else if (*dir == 0)
                  {        make_correct_direction(180); velocity(246,255);  forward_half();  right_drop_seq();   forwarder();        }



                  }








	}




}












//---------------------------------------------------------------------------------
//--------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------





