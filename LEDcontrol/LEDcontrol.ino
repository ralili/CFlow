#include<string.h>
// constants won't change. Used here to 
// set pin numbers:
const int sclkPin =  15;      // the number of the S clock pin
const int sinPin =  16;      // the number of the S in pin
const int xlatPin =  14;      // the number of the X lat pin
const int blankPin =  17;      // the number of the Blank pin
const int gsclkPin =  18;      // the number of the GS clock pin
int i=0;                       // counter for the number of cycles to run
const int cycles=200000;          // number of cycles to run

void setup() {
  
  Serial.begin(9600);
  while (! Serial);
  Serial.println("ready");
  
  // set the digital pin as output:
  pinMode(sclkPin, OUTPUT);
  pinMode(sinPin, OUTPUT);  
  pinMode(xlatPin, OUTPUT);  
  pinMode(blankPin, OUTPUT);  
  pinMode(gsclkPin, OUTPUT);
  
  // set initial pin states:
  digitalWrite(sclkPin, LOW);
  digitalWrite(sinPin, LOW); 
  digitalWrite(xlatPin, LOW); 
  digitalWrite(blankPin, HIGH); 
  digitalWrite(gsclkPin, LOW);
  
  //send initial values to the chip
  __updateGrayscale(blankPin, sclkPin, xlatPin, "111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000");
  


}
//001111101000001111101000001111101000
//000000000000000000000000000000000000
//111111111111111111111111111111111111
//001111101000001111101000001111101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
void loop()
{
  if(i<cycles){
      digitalWrite(blankPin, LOW);
    __grayscaleClock(gsclkPin,0.0);
    __runCycle(4094,gsclkPin,0.0);
    __grayscaleClock(gsclkPin,0.0);
    digitalWrite(blankPin, HIGH);
    i++;
  }

  if(Serial.available()){
    char readChar[12*3*4+1];
    Serial.readBytes(readChar,12*3*4);
    readChar[144]=0;
    Serial.println(readChar);
    __updateGrayscale(blankPin, sclkPin, xlatPin, readChar);
    Serial.flush();
  }
}

void __xlat(int pin, float time){
  digitalWrite(pin, HIGH); 
  delay(time);//miliseconds
  digitalWrite(pin, LOW); 
}

void __serialInput(int pin,int state){
  if(state){
    digitalWrite(pin, HIGH);
  }
  else{
  digitalWrite(pin, LOW);
  }
}

void __serialClock(int pin, float time){
  digitalWrite(pin, HIGH); 
  delay(time);//miliseconds
  digitalWrite(pin, LOW); 
}

void __grayscaleClock(int pin, float time){
  digitalWrite(pin, HIGH); 
  //delay(time);//miliseconds
  digitalWrite(pin, LOW); 
}

void __updateGrayscale(int blankPin, int sclkPin, int xlatPin, char grayscale[192*3]){
  digitalWrite(blankPin, HIGH);
  int i;
  for(i=0;i<strlen(grayscale);i++){
    int state=grayscale[i]-48;
    __serialInput(sinPin,state);
    __serialClock(sclkPin,5);
  }
  __xlat(xlatPin, 50);
}

void __runCycle(int iterations,int gsclkPin,float time){
  int i;
  for(i=0;i<iterations;i++){
    __grayscaleClock(gsclkPin,time);
  }
}
