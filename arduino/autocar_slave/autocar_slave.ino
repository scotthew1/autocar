#include <MatrixController.h>
#include <Wire.h>
#include <string.h>

#define DEBUG

long M1_cur, M2_cur, M1_val, M2_val;  // Motor encoder values
int main_power;  // Driving power; Stored for directional correction
int sensorValue;  // Raw value read from EOPD
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
  readBeagle();
  //EOPDsensor();
  //delay(10);
  /*
  start_motors(15);
  delay(1000);
  nudge(Mx_M1);
  Serial.println("NUDGE");
  delay(1000);
  nudge(Mx_M1);
  Serial.println("NUDGE");
  delay(1000);*/
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
  Mx.SetMode(Mx_M1, FLOAT+SPEED);
  Mx.SetMode(Mx_M2, FLOAT+INV+SPEED);
  main_power = power;  // Store power to manipulate in other functions
  Mx.SetMotors(Mx_M1, power);  // Drive at set power value
  Mx.SetMotors(Mx_M2, power);
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
void inc_power(unsigned char motor, int increment){
  Mx.SetMode(Mx_M1, FLOAT+SPEED);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV+SPEED);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power+increment); // Increment current power by set value
  delay(50);
}
// Decrement Power to single motor
void dec_power(unsigned char motor, int decrement){
  Mx.SetMode(Mx_M1, FLOAT+SPEED);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV+SPEED);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power-decrement); // Decrement current power by set value
  delay(50);
}
// Turn the robot slighty left or right
void nudge(unsigned char motor){
  Mx.SetMode(Mx_M1, FLOAT+SPEED);
  Mx.SetMode(Mx_M2, FLOAT+INV+SPEED);
  inc_power(motor,20);
  delay(75);
  start_motors(main_power);
}
// Start Reverse
void reverse(int power){
  Mx.SetMode(Mx_M1, FLOAT+INV+SPEED);  // Set M1 to Float and Inverse motor direction
  Mx.SetMode(Mx_M2, FLOAT+SPEED);  // Set M2 to Float
  Mx.SetMotors(Mx_M1+Mx_M2, power);  // Reverse at set power value
}
// EOPD Object Detection
void EOPDsensor(){
  if(sensorValue >= 2){
    Serial.write( "eopd" );
    stop_motors();
  }
}
// Read from the Beaglebone and call corresponding function
int readBeagle() {
  int array_max = 4;
  unsigned char _byteData[array_max]; //temp variable for first 4 bits
  unsigned char inChar, byte_motor;
  int inByte, int_power;
  int index = 0; // Index into array; where to store the character#
  if (Serial.available() > 0) {
    // Don't read unless there you know there is data
    inByte = Serial.read();
    while ( inByte != -1 && index < array_max ) {
      _byteData[index] = (unsigned char)inByte;
      index++;
      delay( 5 );
      inByte = Serial.read();
    }
    switch( _byteData[0] ) {
      case 'a':
      // STOP
      Serial.write( "acka" );
      stop_motors();
      break;
      
      case 'b':
      // START
      Serial.write( "ackb" );
      int_power = (int)((_byteData[1]-'0')*10)+(_byteData[2]-'0');
      start_motors( int_power );
      break;
      
      case 'c':
      // TURN LEFT
      Serial.write( "ackc" );
      CCW_90();
      break;
      
      case 'd':
      // TURN RIGHT
      Serial.write( "ackd" );
      CW_90();
      break;
     
      case 'e':
      // TURN AROUND
      Serial.write( "acke" );
      CCW_180();
      break;  
     
      case 'f':
      // Increase Power
      Serial.write( "ackf" );
      byte_motor = ( _byteData[1] );
      int_power = ( _byteData[2] - '0' );
      inc_power( byte_motor, int_power );
      break;
     
      case 'g':
      // Decrease Power
      Serial.write( "ackg" );
      byte_motor = ( _byteData[1] );
      int_power = (int)( _byteData[2] - '0' );
      dec_power( byte_motor, int_power );
      break;
      
      case 'h':
      // REVERSE
      Serial.write( "ackh" );
      int_power = (int)((_byteData[1]-'0')*10)+(_byteData[2]-'0');
      reverse( int_power );
      break;
      
      case 'n':
      // Nudge
      Serial.write( "ackn" );
      nudge(_byteData[1]);
      break;

      case 't':
      // TEST
      Serial.write( "ackt" );
      break;
        
     default:
      // Serial.write( "err" );
      break;
    }
  }
}
