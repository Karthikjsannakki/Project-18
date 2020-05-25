#include<stdio.h>
//#include "distcalc.c"
//#include "netnodecalc.c"



//###############################################################################
// prioritize the list taking the advantages of total node traversal for picks and drops recursively
//###############################################################################
int exists( int x[], int val, int siz)

{
	for( int in=0; in<siz ; in++)

              {    if( x[in] == val )   { return 1;   }
               }
return 0;


}




void   prioritizer( int h[], int  a[], int  n, int s)

{
	int ani[n] ;
	int habi[n];


	   int k = 0;
	   int j=0;
	   int tag = 90;
	   int tag2 = 90; 
           int sourcemarker = 0 ;
	   int  marker = 0; 
	   int dist = 99;
	   int  temp = 0 ;

	 while( marker < n) 
	{
		for( int i = 0; i< n; i++)
		{	int kk = calc_min(a[i],h[i]);

			 temp = distcal(s, a[i]) + distcal( a[i],kk);
			 tag = exists(ani, a[i],n) ;
			 tag2 = exists(habi, h[i], n);


         		if( (temp < dist)  && (tag==0  || tag2==0)    )
 			{            dist = temp ;
				     k = i;
			
			}


		}
		
		habi[j] =  h[k]; 
		ani[j++]  = a[k];

		s  =  calc_min( a[k], h[k]);
		marker++;
		dist = 99;

	}
	
        for (int ass=0 ;ass<n;ass++)
             {    a[ass] = ani[ass]; h[ass] = habi[ass]; }



}
