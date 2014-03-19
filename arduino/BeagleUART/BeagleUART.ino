#define DEBUG
String inData; // Allocate some space for the string
String first4Bits; // the first 4 recieved bits
#include <string.h>


void setup() 
{
  Serial.begin(9600);
}


void loop()
{
  delay(1000);
  if (Serial.available()) {
    readBeagle();
  }
}

int readBeagle() {
  unsigned char* _byteData = (unsigned char*)malloc( sizeof( unsigned char ) * 4); //temp variable for first 4 bits
  unsigned char inChar;
  unsigned char* _speedData = (unsigned char*)malloc( sizeof( unsigned char ) * 3);
  byte index = 0; // Index into array; where to store the character#
  char* outData = (char*)malloc( sizeof(char) * 4);
  delay(1000);
    if (Serial.available() > 0) // Don't read unless there you know there is data
    {
      if ( index < 4 ) {
        inChar = Serial.read(); // Read a character
        _byteData[index] = inChar;
        if (index > 0)
          _speedData[index] = inChar;
        index++;
      }
    }
    switch( _byteData[0] ) {
//      case 0x01:
//        Serial.write("zac");
//        break;
      case 'a':
      // STOP
      #ifdef DEBUG
        Serial.write("a");
      #endif
        break;
      case 'b':
      // START
      #ifdef DEBUG
        Serial.write("b");
      #endif
        break;
      case 'c':
      // TURN LEFT
      #ifdef DEBUG
        Serial.write("c");
      #endif
        break;
      case 'd':
      // TURN RIGHT
      #ifdef DEBUG
        Serial.write("d");
      #endif
        break;
      case 'e':
      // TURN AROUND
      #ifdef DEBUG
        Serial.write("e");
      #endif
        break;  
      case 'f':
      // Increase Power
      #ifdef DEBUG
        Serial.write("f");
      #endif
        break;
      case 'g':
      // Decrease Power
      #ifdef DEBUG
        Serial.write("g");
      #endif
        break;
      case 'h':
      // REVERSE
      #ifdef DEBUG
        Serial.write("h");
      #endif
        break;
        
     default:
        sprintf( outData, "%x", _byteData[0] );
        Serial.write( outData );
        break;
    }
    
    free( _byteData );
    free( _speedData );
    free( outData );
    delay(5000);
}

