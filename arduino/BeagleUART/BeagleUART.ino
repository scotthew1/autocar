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
  byte index = 0; // Index into array; where to store the character#
  char* outData = (char*)malloc( sizeof(char) * 4);
  //Serial.write("1000");
  delay(1000);
    if (Serial.available() > 0) // Don't read unless there you know there is data
    {
      if ( index < 4 ) {
        inChar = Serial.read(); // Read a character
        _byteData[index] = inChar;
        index++;
      }
    }
    switch( _byteData[0] ) {
      case 0x01:
        Serial.write("zac");
        break;
      case 'a':
        Serial.write("a");
        break;
      default:
        sprintf( outData, "%x", _byteData[0] );
        Serial.write( outData );
        break;
    }
    
    free( _byteData );
    free( outData );
    delay(5000);
}

