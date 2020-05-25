
#define F_CPU 14745600
#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>
#include<math.h>
#include<ctype.h>

#include "lcd.h"
#include "travel.c"
#include "netnodecalc.c"
#include "distcalc.c"
#include "locallocator.c"
#include "alphaloc.c"
#include "prioritizer.c"
#include "adjreturn.c"
#include "lastdealer.c"
#include "lastupdate.c"
#include "dirani.c"
#include "placer.c"
#include "arminit.c"
int threshold = 38;

#include<string.h>
long int datain; //to store received data from UDR1

int prevint41 ;
int prevint51;
int prevint42 ;
int prevint52;
int prevint43 ;
int prevint53;
//int datacount();
unsigned char sentdata[32] ;
unsigned char sentdataa[32] ;

unsigned char ADC_Value;
unsigned char sharp, distance, adc_reading;
unsigned int value;
float BATT_Voltage, BATT_V;


unsigned char ADC_Value1;// int
unsigned char ADC_Value2;//int
unsigned char ADC_Value3;//int
unsigned char flag = 0;
unsigned char Left_white_line = 0;
unsigned char Center_white_line = 0;
unsigned char Right_white_line = 0;
int nodecount=0;

int ll,rr;
int i=1 ; int j = 1; int k=0;
int temp1;

int ii=0; 
int kk =0;
 int tem = 0;
  int n =0;

int sig =0 ;

volatile unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
volatile unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
volatile unsigned int Degrees;


unsigned char ADC_Conversion(unsigned char);

void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR5AL = (unsigned char)left_motor;
	OCR5BL = (unsigned char)right_motor;
}

void print_sensor(char row, char coloumn,unsigned char channel)
{
	ADC_Value = ADC_Conversion(channel);
	lcd_print(row, coloumn, ADC_Value, 3);
}



unsigned int Sharp_GP2D12_estimation(unsigned char adc_reading)
{
	float distance;
	unsigned int distanceInt;
	distance = (int)(10.00*(2799.6*(1.00/(pow(adc_reading,1.1546)))));
	distanceInt = (int)distance;
	if(distanceInt>800)
	{
		distanceInt=800;
	}
	return distanceInt;
}


unsigned char ADC_Conversion(unsigned char Ch)
{
	unsigned char a;
	if(Ch>7)
	{
		ADCSRB = 0x08;
	}
	Ch = Ch & 0x07;
	ADMUX= 0x20| Ch;
	ADCSRA = ADCSRA | 0x40;		//Set start conversion bit
	while((ADCSRA&0x10)==0);	//Wait for ADC conversion to complete
	a=ADCH;
	ADCSRA = ADCSRA|0x10; //clear ADIF (ADC Interrupt Flag) by writing 1 to it
	ADCSRB = 0x00;
	return a;
}



void adc_init()
{
	ADCSRA = 0x00;
	ADCSRB = 0x00;		//MUX5 = 0
	ADMUX = 0x20;		//Vref=5V external --- ADLAR=1 --- MUX4:0 = 0000
	ACSR = 0x80;
	ADCSRA = 0x86;		//ADEN=1 --- ADIE=1 --- ADPS2:0 = 1 1 0
}

void timer5_init()
{
	TCCR5B = 0x00;	//Stop
	TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT5L = 0x01;	//Counter lower 8-bit value to which OCR5xH value is compared with
	OCR5AH = 0x00;	//Output compare register high value for Left Motor
	OCR5AL = 0xFF;	//Output compare register low value for Left Motor
	OCR5BH = 0x00;	//Output compare register high value for Right Motor
	OCR5BL = 0xFF;	//Output compare register low value for Right Motor
	OCR5CH = 0x00;	//Output compare register high value for Motor C1
	OCR5CL = 0xFF;	//Output compare register low value for Motor C1
	TCCR5A = 0xA9;	/*{COM5A1=1, COM5A0=0; COM5B1=1, COM5B0=0; COM5C1=1 COM5C0=0}
 					  For Overriding normal port functionality to OCRnA outputs.
				  	  {WGM51=0, WGM50=1} Along With WGM52 in TCCR5B for Selecting FAST PWM 8-bit Mode*/
	
	TCCR5B = 0x0B;	//WGM12=1; CS12=0, CS11=1, CS10=1 (Prescaler=64)
}



void init_devices()
{
	cli(); 
	port_init();
	timer1_init();
	adc_init();
	timer5_init();
	left_position_encoder_interrupt_init();
    right_position_encoder_interrupt_init();		
	uart2_init();
	sei();  
}




void buzzer_pin_config (void)
{
	DDRC = DDRC | 0x08;		//Setting PORTC 3 as outpt
	PORTC = PORTC & 0xF7;		//Setting PORTC 3 logic low to turnoff buzzer
}

void motion_pin_config (void)
{
	DDRA = DDRA | 0x0F;
	PORTA = PORTA & 0xF0;
	DDRL = DDRL | 0x18;   //Setting PL3 and PL4 pins as output for PWM generation
	PORTL = PORTL | 0x18; //PL3 and PL4 pins are for velocity control using PWM.
}



void left_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xEF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x10; //Enable internal pull-up for PORTE 4 pin
}

void right_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xDF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x20; //Enable internal pull-up for PORTE 4 pin
}

void left_position_encoder_interrupt_init (void) //Interrupt 4 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x02; // INT4 is set to trigger with falling edge
	EIMSK = EIMSK | 0x10; // Enable Interrupt INT4 for left position encoder
	sei();   // Enables the global interrupt
}

void interrupt_switch_config (void)
{
	DDRE = DDRE & 0x7F;  //PORTE 7 pin set as input
	PORTE = PORTE | 0x80; //PORTE7 internal pull-up enabled
}

void right_position_encoder_interrupt_init (void) //Interrupt 5 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x08; // INT5 is set to trigger with falling edge
	EIMSK = EIMSK | 0x20; // Enable Interrupt INT5 for right position encoder
	sei();   // Enables the global interrupt
}

ISR(INT5_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}

ISR(INT4_vect)
{
	ShaftCountLeft++;  //increment left shaft position count
}


void motion_set (unsigned char Direction)
{
	unsigned char PortARestore = 0;

	Direction &= 0x0F; 		// removing upper nibbel for the protection
	PortARestore = PORTA; 		// reading the PORTA original status
	PortARestore &= 0xF0; 		// making lower direction nibbel to 0
	PortARestore |= Direction; // adding lower nibbel for forward command and restoring the PORTA status
	PORTA = PortARestore; 		// executing the command
}

void forward (void) //both wheels forward
{
	motion_set(0x06);
}

void back (void) //both wheels backward
{
	motion_set(0x09);
}

void left (void) //Left wheel backward, Right wheel forward
{
	motion_set(0x05);
}

void right (void) //Left wheel forward, Right wheel backward
{
	motion_set(0x0A);
}

void soft_left (void) //Left wheel stationary, Right wheel forward
{
	motion_set(0x04);
}

void soft_right (void) //Left wheel forward, Right wheel is stationary
{
	motion_set(0x02);
}

void soft_left_2 (void) //Left wheel backward, right wheel stationary
{
	motion_set(0x01);
}

void soft_right_2 (void) //Left wheel stationary, Right wheel backward
{
	motion_set(0x08);
}

void stop (void)
{
	motion_set(0x00);
}

//Function used for turning robot by specified degrees
void angle_rotate(unsigned int Degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) Degrees/ 4.090; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	while (1)
	{
		if((ShaftCountRight >= ReqdShaftCountInt) | (ShaftCountLeft >= ReqdShaftCountInt))
		break;
	}
	stop(); //Stop robot
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = DistanceInMM / 5.338; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	while(1)
	{
		if(ShaftCountRight > ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}

void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}


void forward_half(unsigned int DistanceInMM)
{
	forward();
	
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = 28.100412139378044; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	ShaftCountLeft = 0;
	
	while(1)
	{   
		
		
				Left_white_line= ADC_Conversion(3);
				Center_white_line = ADC_Conversion(2);
				Right_white_line = ADC_Conversion(1);
		forward();
		
		if(Left_white_line <= threshold && Center_white_line <= threshold && Right_white_line >= threshold)
		
		{
			velocity(250,200);
		}
		
		
		if(Left_white_line <= threshold && Center_white_line >=threshold && Right_white_line >= threshold)
		
		{
			velocity(250,220);
		}
		
		
		if(Left_white_line <= threshold && Center_white_line >=threshold && Right_white_line <= threshold)
		
		{
			velocity(246,255);
		}
		
		
		
		if(Left_white_line >= threshold && Center_white_line <=threshold && Right_white_line <= threshold)
		
		{
			velocity(200,250);
		}
		
		
		if(Left_white_line >= threshold && Center_white_line >=threshold && Right_white_line <= threshold)
		
		{
			velocity(220,250);
		}
		
		
		if(ShaftCountRight  > ReqdShaftCountInt  ||   ShaftCountLeft  > ReqdShaftCountInt)
		{
			break;
		}
		
		
	}
	stop();
			
}







void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

void left_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	left(); //Turn left
	angle_rotate(Degrees);
}



void right_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	right(); //Turn right
	angle_rotate(Degrees);
}


void soft_left_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_left(); //Turn soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_right();  //Turn soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_left_2_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_left_2(); //Turn reverse soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_2_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_right_2();  //Turn reverse soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}







void make_correct_direction (int dir)
{
	if (dir==90)
	{
		forward_cus();
	}
	



	else if(dir==180)
	{   
		
	
		left_rotate();
		

	}
	
	
	else if(dir==-90)
	{
		
		
		oneighty_rotate();
		

	}
	
	
	else
	{  
		
				
		right_rotate();
		
		
	}
}






void dojob()
{
	Left_white_line = ADC_Conversion(3);
	Center_white_line = ADC_Conversion(2);
	Right_white_line = ADC_Conversion(1);
	
			print_sensor(2,2,3);
			print_sensor(2,6,2);
			print_sensor(2,10,1);
}


void lr_cus(int xxx)
{

	
	

	
	make_correct_direction(xxx);
	
	forwarder();


}







void forward_cus()
{
	
	velocity(246,255);

	forward_mm(4*10);
    forwarder();

}





void something()
{
	DDRB = DDRB | 0x20; //making PORTB 5 pin output
	PORTB = PORTB | 0x20; //setting PORTB 5 pin to logic 1
	DDRB = DDRB | 0x40; //making PORTB 6 pin output
	PORTB = PORTB | 0x40; //setting PORTB 6 pin to logic 1
	DDRB = DDRB | 0x80; //making PORTB 7 pin output
	PORTB = PORTB | 0x80; //setting PORTB 7 pin to logic 1	
}




void timer1_init()
{
	TCCR1A = 0x00;
	
	ICR1 = 1023; //TOP = 1023
	TCNT1H = 0xFC; //Counter high value to which OCR1xH value is to be compared with
	TCNT1L = 0x01; //Counter low value to which OCR1xH value is to be compared with
	OCR1A = 1023;
	OCR1B = 1023;
	OCR1C = 1023;
	TCCR1A = 0xAB;

	TCCR1B = 0x0C; //WGM12=1; CS12=1, CS11=0, CS10=0 (Prescaler=256)
}

void servo_1(unsigned char degrees)
{
	float regval = ((float)degrees * 0.512) + 34.56;
	OCR1A = (uint16_t) regval;
}

//Sets servo 2 to the specified angle in degrees
void servo_2(unsigned char degrees)
{
	float regval = ((float)degrees * 0.512) + 34.56;
	OCR1B = (uint16_t) regval;
}

//Sets servo 3 to the specified angle in degrees
void servo_3(unsigned char degrees)
{
	float regval = ((float)degrees * 0.512) + 34.56;
	OCR1C = (uint16_t) regval;
}




void port_init()

{	something();
	lcd_port_config();
	motion_pin_config();
	buzzer_pin_config();
	left_encoder_pin_config();
	right_encoder_pin_config();
	interrupt_switch_config();
}

void buzzer_on (void)
{
	unsigned char port_restore = 0;
	port_restore = PINC;
	port_restore = port_restore | 0x08;
	PORTC = port_restore;
}

void buzzer_off (void)
{
	unsigned char port_restore = 0;
	port_restore = PINC;
	port_restore = port_restore & 0xF7;
	PORTC = port_restore;
}




void uart2_init(void)
{
	UCSR2B = 0x00; //disable while setting baud rate
	UCSR2A = 0x00;
	UCSR2C = 0x06;
	UBRR2L = 0x5F; //set baud rate lo
	UBRR2H = 0x00; //set baud rate hi
	UCSR2B = 0x98;
}


SIGNAL(SIG_USART2_RECV) 		
{
	datain = UDR2; 				
	if(datain != '#' )
	
	{
		sentdata[k] = datain;
		
//###############################################################################
//LCD printing logic
//###############################################################################

		
	if( sentdata[k] == '\n') { i = 2; j=1; k++;}
	lcd_cursor(i,j);
if(sentdata[k] != '\n' && sentdata[k] != '\0')  { lcd_wr_char(sentdata[k]);
	
	k++; j++;}



	  }	
	  		
	else
	     {
			
			sentdata[k] = '#'; sentdata[k+1]='\0'; lcd_wr_command(0x0C);
		
//###############################################################################
//Extracting the logic data
//###############################################################################	
		 
			i=0;
		  j=0; 
		  for(k=0; sentdata[k] != '#'; k++)   
		  {
		  if(j==16) { }
			  if (sentdata[k] == '\n') {    sentdataa[i++] = sentdata[k]   ;  j=1; }
			  if(    sentdata[k] != '\0' && sentdata[k] != '\n' ) {    sentdataa[i++] =    sentdata[k];         
		 j++; }
	       }
		
		sentdataa[i] ='\0';
		
		k=99;
		



          i=1 ;  
          j = 1; 
		  ii=0;
		  kk =0;
	      tem = 0;
		  n =0;
		
		if(   k==99   ) 
	{   
		
		
		
		while(  (PINE & 0x80) == 0x80      ) {}
	
//###############################################################################
//Entry point after boot switch
//###############################################################################	
	
	
	
	
	
		
		init_devices();
		lcd_set_4bit();
		lcd_init();
		velocity(246,255); 

//###############################################################################
//Extraction of numeric value which is number of associations
//###############################################################################		
		n=0; kk=0;
		while( sentdataa[kk] != '\n')
		{
			  if(sentdataa[kk] == ',')
		             { n++;    
					  }
			kk++;

		}
		

		n++;
		kk=0;



		int habis[n];
		char animals[2*n] ;



//###############################################################################
//Extraction of habitats 
//###############################################################################

		
		
		
		while(sentdataa[ii] != '\n')
		{
			if( sentdataa[ii] != ',')
			{
				if(isdigit(sentdataa[ii]))
				{

					tem =  sentdataa[ii] - '0' ;
					if( isdigit(sentdataa[ii+1]) && sentdataa[ii+1] != '\n')
					{ tem  = 10*tem +  sentdataa[ii+1] - '0';  ii++;
					}

					habis[kk++] = tem; tem = 0;
				}
			}

			ii++;
		}
		//--
	

//###############################################################################
//Extraction of   animals
//###############################################################################
	
	kk=0;
	for(ii; sentdataa[ii] != '\0' ; ii++)

	{   
		if(isalpha(sentdataa[ii]) || isdigit(sentdataa[ii]))

		{   animals[kk++]=sentdataa[ii];  

		}
    
	}
	
	

//###############################################################################
//Calculating of b co-ordinate of each habitat as a reference co-ordinate 
// co ordinate associated with an habitat are a,b,c,d
//   eyantra logo
//		d-------c
//      |       |
//      |       | 
//      a-------b
// 
//###############################################################################
	
	
	int  habit_b_cords[n] ;

	for(ii=0; ii<n; ii++)
	{        habit_b_cords[ii] = lfind( habis[ii]);


	}
	

//###############################################################################
//Extraction of animal locations that are connected to co ordinates of habitats straight away
//###############################################################################	
	
	int animals_cords[n];
	kk = 0;
	
	for(ii=0;ii<2*n;ii=ii+2)
     {  animals_cords[kk++] =  func( animals[ii], animals[ii+1]); 
	 }



//###############################################################################
//prioritizing the processed list for near pick and drops recursively
//###############################################################################

      prioritizer(habit_b_cords, animals_cords, n, 0);


      int  travel_list[2*n];

//###############################################################################
//another list stores single co ordinate  of habitat  which is most near to associated animal
//###############################################################################
       int another_list[n];

       for( ii=0 ; ii<n ; ii++)
       {
	       another_list[ii] = calc_min(animals_cords[ii], habit_b_cords[ii]);


        }

//###############################################################################
//copying animals  to a array in a  manner habitat and animal way    
//###############################################################################
	
    ii=0;
    while( ii < 2*n)
    {

	travel_list[ii] =   animals_cords[ii];
	ii= ii+2;
   }


    int jj=0 ;
    int z =0;

//###############################################################################
//merging habitat co ordinates which is near to associated animals
//###############################################################################	
    
for(ii=0; ii<2*n ;  ii++)
{
if(ii%2 != 0) {  travel_list[ii] = another_list[jj++];   }
    else  { travel_list[ii] = animals_cords[z++];  }



}


//###############################################################################
//creating a last array containing order of co ordinates t be traversed 
//###############################################################################

int last_list[2*n];
kk=0;
jj=0;
for(ii=0 ; ii<2*n; ii++)
{
	if(ii>0 && ii< 2*n && ii%2 == 0) {
		last_list[kk]= adjplease( habit_b_cords[jj++], travel_list[ii-1], travel_list[ii]);
		last_list[++kk] = travel_list[ii];
	}
	

	else{
		

		last_list[kk] = travel_list[ii];
	}
	kk++;

}



//###############################################################################
// beginning of traversal from source node which is 0,0
//###############################################################################

	
int source = 0;
int direction = 90;

ii =0;
jj=0;	

int tracer = 2*n + n-1;
int lasttmp =1;
int lastcmp = 0;
int lastmrk  = 1;
int prevdir = 0;



while( ii< 2*n+(n-1) )




{
	 lasttmp = ++lasttmp % 3 ;
	while(  source !=   last_list[ii]   )

	{


		
       //###############################################################################
       //traversing recursively to the co ordinates in last list
       //###############################################################################
		source =  travell(source,last_list[ii], &direction);
		prevdir = direction;
       stop(); 
	  

	} 
        tracer--;

	if ( source  == last_list[ii]  )
	{

		if( ii%3 == 0)
	    {  //###############################################################################
		    //picks the animal block
		    //###############################################################################
			stop();
			resol( last_list[ii] , &direction);

	    }
	
	    if( lasttmp == 0 )
					//###############################################################################
					//drops the  animal block
					//###############################################################################
	     {		   stop();
		       	   placeit(last_list[ii], last_list[ii+1], habit_b_cords[jj++], &direction ) ;
		       	   source =  lup(last_list[ii], last_list[ii+1], &direction);
					  
		       	   
	     }
	
	
	}	ii++;
	
	
	}
	
		
						//###############################################################################
						//deals with the last node 
						//###############################################################################

     if(tracer == 0) {    deallast(last_list[2*n-1 + n-1], habit_b_cords[n-1], &prevdir);  buzzer_on(); _delay_ms(5000) ; buzzer_off();       } 

                     
					
					  }




	}


	
		
		
		  
		
		
		
 }		
		
//###############################################################################
//left turn
//###############################################################################		


void left_rotate()
{
	
	velocity(246,255);
	forward_mm(75);
	
	left_degrees(70);

	
	
	Center_white_line = ADC_Conversion(2);
	Right_white_line = ADC_Conversion(1);
	while(Center_white_line < threshold && Right_white_line < threshold ){
		
		
		left();
		_delay_ms(100);
		stop();
		Center_white_line = ADC_Conversion(2);
			Right_white_line = ADC_Conversion(1);
	}

	velocity(246,255);
	
}

//###############################################################################
//right turn
//###############################################################################
void right_rotate()
{
	
	velocity(246,255);
	forward_mm(75);
	
	right_degrees(70);
	
	
	Left_white_line = ADC_Conversion(3);
		Center_white_line = ADC_Conversion(2);
	while( Center_white_line < threshold &&  Left_white_line < threshold){
		right();
		_delay_ms(100);
		stop();
		Left_white_line = ADC_Conversion(3);
			Center_white_line = ADC_Conversion(2);
	}

	
	
}



//###############################################################################
//180 degree right rotate
//###############################################################################
void oneighty_rotate()
{
	
	velocity(246,255);
	forward_mm(75);
	
	right_degrees(70);
	
	Left_white_line = ADC_Conversion(3);
	Center_white_line = ADC_Conversion(2);
	while( Center_white_line < threshold &&  Left_white_line < threshold){
		
		
		right();
		_delay_ms(100);
		stop();
		Left_white_line = ADC_Conversion(3);
		Center_white_line = ADC_Conversion(2);
	}
	
	right_degrees(70);
	
	Left_white_line = ADC_Conversion(3);
	Center_white_line = ADC_Conversion(2);
	while( Center_white_line < threshold &&  Left_white_line < threshold){
		
		
		right();
		_delay_ms(100);
		stop();
		Left_white_line = ADC_Conversion(3);
		Center_white_line = ADC_Conversion(2);
	}

}






	
//###############################################################################
//animal left pick sequence
//###############################################################################

void left_pick_seq()
{
	
	servo_1(0);
	_delay_ms(1000);
	
	servo_2(0);
	_delay_ms(1000);
	
	
	servo_3(70);
	_delay_ms(1000);
	
	servo_2(180);
	_delay_ms(1000);
	
	servo_1(90);
	_delay_ms(1000);
	
}

//###############################################################################
//animal left drop sequence
//###############################################################################

void left_drop_seq()
{
	
	servo_1(0);
	_delay_ms(1000);
	
	servo_2(10);
	_delay_ms(1000);
	
	
	servo_3(180);
	_delay_ms(1000);
	
	servo_2(150);
	_delay_ms(1000);
	
	servo_1(90);
	_delay_ms(1000);
	
}

//###############################################################################
//animal right drop sequence
//###############################################################################

void right_drop_seq()
{
	
	servo_1(180);
	_delay_ms(1000);
	
	servo_2(10);
	_delay_ms(1000);
	
	
	servo_3(180);
	_delay_ms(1000);
	
	servo_2(150);
	_delay_ms(1000);
	
	servo_1(90);
	_delay_ms(1000);
	
}

//###############################################################################
//animal right pick sequence
//###############################################################################

void right_pick_seq()
{
	
	servo_1(180);
	_delay_ms(1000);
	
	servo_2(0);
	_delay_ms(1000);
	
	
	servo_3(70);
	_delay_ms(1000);
	
	servo_2(150);
	_delay_ms(1000);
	
	servo_1(90);
	_delay_ms(1000);
	
}

//###############################################################################
//animal front pick sequence
//###############################################################################

void front_seq()
{
	
	servo_1(90);
	_delay_ms(1000);
	
	servo_2(0);
	_delay_ms(1000);
	
	
	servo_3(70);
	_delay_ms(1000);
	
	servo_2(150);
	_delay_ms(1000);
	
	servo_1(90);
	_delay_ms(1000);
	
}


//###############################################################################
//servo initializer to the desired position
//###############################################################################

void servo_init()
{
	servo_2(150); _delay_ms(1000);
	servo_1(90); _delay_ms(1000);
	servo_3(180); _delay_ms(1000);
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//###############################################################################
//line follower till the front node
//###############################################################################
void forwarder()
{
	
	while(1)
	{
		Left_white_line= ADC_Conversion(3);
		Center_white_line = ADC_Conversion(2);
		Right_white_line = ADC_Conversion(1);
		

		
		
		forward();
		
		if(Left_white_line <= threshold && Center_white_line <= threshold && Right_white_line >= threshold)
		
		{
			velocity(250,200);
		}
		
		
		if(Left_white_line <= threshold && Center_white_line >=threshold && Right_white_line >= threshold)
		
		{
			velocity(250,220);
		}
		
		
		if(Left_white_line <= threshold && Center_white_line >=threshold && Right_white_line <= threshold)
		
		{
			velocity(246,255);
		}
		
		
		
		if(Left_white_line >= threshold && Center_white_line <=threshold && Right_white_line <= threshold)
		
		{
			velocity(200,250);
		}
		
		
		if(Left_white_line >= threshold && Center_white_line >=threshold && Right_white_line <= threshold)
		
		{
			velocity(220,250);
		}
		
		
		if(Left_white_line >= threshold && Center_white_line >=threshold && Right_white_line >= threshold)
		
		{
			velocity(0,0);
			buzzer_on();
			_delay_ms(100);
			buzzer_off();
			stop();
			break;
		}
		
		
		
		
	}
	
	
	
	
}





//###############################################################################
//animal corner left pick sequence
//###############################################################################

void slight_left_seq()
{
	velocity(246,255);
	forward_mm(125);
	left_pick_seq();
	back_mm(125);	
	
	
}

//###############################################################################
//animal at starting node pick sequence
//###############################################################################

void slight_down_left_seq()
{
	

	back_mm(125);
	left_pick_seq();
	forward_mm(125);
	
	
}





//###############################################################################
//animal corner right  pick sequence
//###############################################################################

void slight_right_seq()
{		velocity(246,255);
		forward_mm(125);
		right_pick_seq();
		back_mm(125);
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Main Function



int main(void)
{
	init_devices();
	lcd_set_4bit();
	lcd_init();
    velocity(246,255);
	
	// servo initializer
	servo_init();


	
	while(1)
	
	{
		
	}
	
	
	//###################################################################3
	//    
	//   arena lies in  xy plane
	// every node has a co ordinate and a two digit number, 10th place has x co ordinate unit place has y co ordinate
	
	// eyantra logo is considered as north,   0 degrees is x axis 90 degrees is towards eyantra logo 180 is -x axis and -90 is -y axis
	//  after trying all permutaions of all possible animals habitat associations we have got 44 node to node traversals
	// while the current gives 48 traversals,  we are about to find the algorithm which gets to minimal traversal in sample space
    //##########################################
		
	

    }	
		
		
	

