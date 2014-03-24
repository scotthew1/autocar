#include <Wire.h>
#include <string.h>

int loopCount = 0;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}`

void loop() {
  int inByte, i;
  int byteArray[4];
  
  if ( Serial1.available() > 0 ) {
    Serial.print( "loop " );
    Serial.print( loopCount++ );
    Serial.println( ':' );
    i = 0;
    inByte = Serial1.read();
    while ( inByte != -1 && i < 4 ) {
      delay(1);
      byteArray[i] = inByte;
      inByte = Serial1.read();
      i++;
    }
    Serial1.flush();
    Serial1.write( byteArray[0] );
    Serial.print( byteArray[0] );
    Serial.print( ' ' );
    Serial.print( byteArray[1] );
    Serial.print( ' ' );
    Serial.print( byteArray[2] );
    Serial.print( ' ' );
    Serial.println( byteArray[3] );
  }
  
}
