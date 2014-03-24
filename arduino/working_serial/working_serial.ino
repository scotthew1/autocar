#include <Wire.h>
#include <string.h>

int loopCount = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int inByte, i;
  char byteArray[4];
  
  if ( Serial.available() > 0 ) {
    i = 0;
    inByte = Serial.read();
    while ( inByte != -1 && i < 4 ) {
      delay(5);
      byteArray[i] = (char)inByte;
      inByte = Serial.read();
      i++;
    }
    Serial.flush();
//    Serial.write( byteArray[0] );
    switch ( byteArray[0] ) {
      case 'a':
        Serial.write( "acka" );
        break;
      case 'b':
        Serial.write( "ackb" );
        break;
      case 't': 
        Serial.write( "ackt" );
        break;
      default:
        break;
    }
  }
  
}
