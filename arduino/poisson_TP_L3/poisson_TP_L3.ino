#include <avr/io.h>
#include <avr/interrupt.h>

#define MAX_BUFF_EVT          1900 //fixe le nombre de mesure par experience
//#define MAX_BUFF_EVT_MINUS_1  1999 
#define MAX_16BIT_TIMER       65535
#define NB_OF_EXPERIMENT      1    //fixe le nombre d'experience

//#define CAPTURE_INPUT_PIN     8
#define CAPTURE_INPUT_PIN     48
#define RESET_PIN             10

void printDataToSerial();

// Contient le temps d'arrivée en tick horloge. Ici le tick horloge fait 64µs, avec 
unsigned long evt[MAX_BUFF_EVT];
volatile int nbEvt;
volatile int overflow_;
unsigned short nb_char;
unsigned short max_char = 8;

char buffer_entree[3];

void initTimer() //initialise le timer
{

  TCCR5A = 0;
  TCCR5B = 0;
  TCNT5  = 0;
  TCCR5B |= (0 <<  ICNC5) | (1 << ICES5); //desactive le filtre de noice canceling pour avoir une meilleure resolution temporelle et permet d'effectuer une detection en front montant  
  TCCR5B |=  (1 << CS52) |(0 << CS51) | (1 << CS50);  // permet d'avoir une resolution temporelle /1024, de l'ordre de 64 microsecondes   
  TIFR5 = (1<<ICF5) | (1<<TOV5);    // efface l'attente  
  TIMSK5 |= (1 << TOIE5) | (1 << ICIE5); //active l'interruption quand le timer5 deborde      
  }
  
void stopTimer() //arrete le timer
{  
  TIMSK5 = 0;
}

void restartTimer() //restarts the timer
{
  TIMSK5 |= (1 << ICIE5);  //declenche une interruption lorsque le timer deborde (overflow)
}


void startExperiment() //lance l'experience 
{
  //Serial.print("Start"); 
  nbEvt = 0;  
  overflow_ = 0;  
  initTimer();  
}

// le programme se lance lorsqu'on appuie sur reset:
void setup() {
  Serial.begin(57600); //initialise la communication avec le serial moniteur a 9600 bps  
  //Serial.println("Setup !"); 
  pinMode(RESET_PIN, INPUT_PULLUP);
  pinMode(CAPTURE_INPUT_PIN, INPUT);

  //startExperiment();   
}

ISR(TIMER5_OVF_vect)   //Interrupt service run, declenche une interruption lorsque le timer deborde  
{
  overflow_ += 1;
  //Serial.println("Overflow !"); //affiche overflow sur l'ecran quand le timer deborde
  //Serial.println(overflow_); 

}

ISR(TIMER5_CAPT_vect) //declenche une capture d'impulsion
{

  //Serial.println("Capture !");  //affiche capture a l'ecran lors de la capture d'une impulsion
  evt[nbEvt] = ICR5 + MAX_16BIT_TIMER * overflow_;

  Serial.println(evt[nbEvt]);
  nbEvt++;     
  
         
    if(nbEvt == MAX_BUFF_EVT)
    {        
    stopTimer();
    //transfertDataToSD();   
    printDataToSerial();  //prints all acquired data on the serial monitor
    }
}

void restartAllTheExperiment()
{ 
  startExperiment();   
}



void printDataToSerial()
{
    for(int j=0; j < nbEvt; j++)
    {
    Serial.println(evt[j]);   
    }    
}


// the loop routine runs over and over again forever:
void loop() {  

////wait for a pseudo reset button
//if(digitalRead(RESET_PIN) == LOW)
//  {
//  Serial.println("Restarting"); 
//  restartAllTheExperiment();
//  }
//          
}


void serialEvent() {
   if (Serial.available() > 0){
      nb_char = Serial.readBytesUntil ('/', buffer_entree, max_char);
      DecodageSerial(); 
   }
} 

void DecodageSerial () {
//Serial.println(buffer_entree);

  if(buffer_entree[0] == 'c')
  {
    // c for count
    startExperiment();
  }
  else if (buffer_entree[0] == 's')
  {
    // s for stop
    stopTimer();
  }    
  else if (buffer_entree[0] == 'e')
  {
    // i for export
    printDataToSerial();
  }   
     
  else if (buffer_entree[0] == '?')
  {
   Serial.println("Poisson/");
  } 
   
}




