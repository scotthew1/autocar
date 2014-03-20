#include <MatrixController.h>
#include <Wire.h>
#include <string.h>

#define DEBUG

long M1_cur, M2_cur, M1_val, M2_val;  // Motor encoder values
int main_power;  // Driving power; Stored for directional correction
int sensorValue = analogRead(A0);  // Raw value read from EOPD
int calcValue = 0;  // Distance value in milimeters
String inData;  // Allocate some space for string
String first4Bits;  // The first 4 recieved bits

void setup(){
  Serial.begin(9600);
}
// This Interupt is required by the Matrix Library
ISR(TIMER1_COMPA_vect){
  Mx.MatrixController_ISR();
}

void loop(){
  /*delay(500);
  if(Serial.available()){
    readBeagle();
  }*/
  // This is TEST code!
  Serial.println("CCW_90 : Making Left Turn");
  CCW_90();
  delay(5000);
  Serial.println("start_motors");
  start_motors(50);
  delay(5000);
  Serial.println("stop_motors");
  stop_motors();
  delay(5000);
  Serial.println("CW_90 : Making Right Turn");
  CW_90();
  delay(5000);
  Serial.println("start_motors");
  start_motors(50);
  delay(5000);
  Serial.println("stop_motors");
  stop_motors();
  delay(5000);
  Serial.println("CCW_180 : Turn Around");
  CCW_180();
  delay(5000);
  Serial.println("start_motors");
  start_motors(50);
  delay(5000);
  Serial.println("stop_motors");
  stop_motors();
  delay(5000);
}
// Left Turn
void CCW_90(){  
  Mx.SetMode(Mx_M1, SLEW);  // Set M1 to Slew
  Mx.SetMode(Mx_M2, SLEW);  // Set M2 to Slew
  M1_cur = Mx.MotorPosition(Mx_M1);  // Get M1 current encoder value
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);  // Get M2 current encoder value
  M1_val = M1_cur + 415;
  M2_val = M2_cur + 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);  // Reset M1
  Mx.SetMode(Mx_M2, RESET);  // Reset M2
}
// Right Turn
void CW_90(){  
  Mx.SetMode(Mx_M1, SLEW);  // Set M1 to Slew
  Mx.SetMode(Mx_M2, SLEW);  // Set M2 to Slew
  M1_cur = Mx.MotorPosition(Mx_M1);  // Get M1 current encoder value
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);  // Get M2 current encoder value
  M1_val = M1_cur - 415;
  M2_val = M2_cur - 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);  // Reset M1
  Mx.SetMode(Mx_M2, RESET);  // Reset M2
}
// Turn Around
void CCW_180(){  
  Mx.SetMode(Mx_M1, SLEW);  // Set M1 to Slew
  Mx.SetMode(Mx_M2, SLEW);  // Set M2 to Slew
  M1_cur = Mx.MotorPosition(Mx_M1);  // Get M1 current encoder value
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);  // Get M2 current encoder value
  M1_val = M1_cur + 825;
  M2_val = M2_cur + 825;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);  // Reset M1
  Mx.SetMode(Mx_M2, RESET);  // Reset M2
}
// Start Driving
void start_motors(int power){
  Mx.SetMode(Mx_M1, FLOAT);
  Mx.SetMode(Mx_M2, FLOAT+INV);
  main_power = power;  // Store power to manipulate in other functions
  Mx.SetMotors(Mx_M1+Mx_M2, power);  // Drive at set power value
}
// Stop Motors
void stop_motors(){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT);  // Set M2 to Float
  Mx.SetMotors(Mx_M1+Mx_M2, 0);  // Set Motor Power to 0
  delay(500);
  Mx.SetMode(Mx_M1, RESET);  // Reset M1
  Mx.SetMode(Mx_M2, RESET);  // Reset M2
}
// Increment Power to single motor
void inc_power(char motor, int increment){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power+increment); // Increment current power by set value
  delay(500);
}
// Decrement Power to single motor
void dec_power(char motor, int decrement){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power-decrement); // Decrement current power by set value
  delay(500);
}
// Start Reverse
void reverse(int power){
  Mx.SetMode(Mx_M1, FLOAT+INV);  // Set M1 to Float and Inverse motor direction
  Mx.SetMode(Mx_M2, FLOAT);  // Set M2 to Float
  Mx.SetMotors(Mx_M1+Mx_M2, power);  // Reverse at set power value
}
// EOPD Object Detection
void EOPDsensor(){
  //Convert raw value of(24-724) to milimeters
  if(sensorValue > 200){
    calcValue = ((524.88/sqrt(sensorValue))-15.29);
  }
  else{
    calcValue = ((524.88/sqrt(sensorValue))-21.29);
  } 
  //Figure out threshold for distance checking.
  //What distance will trigger EOPD?
  //EOPD run multiple check to confirm object?
}
int readBeagle() {
  unsigned char* _byteData = (unsigned char*)malloc( sizeof( unsigned char ) * 4); //temp variable for first 4 bits
  unsigned char inChar;
  unsigned char* _speedData = (unsigned char*)malloc( sizeof( unsigned char ) * 3);
  int byte_power, byte_motor;
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
      stop_motors();
      #ifdef DEBUG
        Serial.write("a");
      #endif
        break;
      
      case 'b':
      // START
      byte_power = ((_byteData[1]-'0')*10)+(_byteData[2]-'0');
      start_motors(byte_power);
      #ifdef DEBUG
        Serial.write("b");
      #endif
        break;
      
      case 'c':
      // TURN LEFT
      CCW_90();
      #ifdef DEBUG
        Serial.write("c");
      #endif
        break;
      
      case 'd':
      // TURN RIGHT
      CW_90();
      #ifdef DEBUG
        Serial.write("d");
      #endif
        break;
     
      case 'e':
      // TURN AROUND
      CCW_180();
      #ifdef DEBUG
        Serial.write("e");
      #endif
        break;  
     
      case 'f':
      // Increase Power
      byte_power = (_byteData[2]-'0');
      byte_motor = (_byteData[1]-'0');
      inc_power(byte_motor,byte_power);
      #ifdef DEBUG
        Serial.write("f");
      #endif
        break;
     
      case 'g':
      // Decrease Power
      byte_power = (_byteData[2]-'0');
      byte_motor = (_byteData[1]-'0');
      dec_power(byte_motor,byte_power);
      #ifdef DEBUG
        Serial.write("g");
      #endif
        break;
      
      case 'h':
      // REVERSE
      byte_power = ((_byteData[1]-'0')*10)+(_byteData[2]-'0');
      reverse(byte_power);
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
