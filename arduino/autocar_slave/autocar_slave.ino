#include <MatrixController.h>
#include <Wire.h>

long M1_cur, M2_cur, M1_val, M2_val;  // Motor encoder values
int main_power;  // Driving power; Stored for directional correction
int sensorValue = analogRead(A0);  // Raw value read from EOPD
int calcValue = 0;  // Distance value in milimeters

void setup(){
  Serial.begin(9600);
}
// This Interupt is required by the Matrix Library
ISR(TIMER1_COMPA_vect){
  Mx.MatrixController_ISR();
}

void loop(){
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
// Start Reverse
void reverse(int power){
  Mx.SetMode(Mx_M1, FLOAT+INV);  // Set M1 to Float and Inverse motor direction
  Mx.SetMode(Mx_M2, FLOAT);  // Set M2 to Float
  Mx.SetMotors(Mx_M1+Mx_M2, power);  // Reverse at set power value
}
// Stop Motors
void stop_motors(){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT);  // Set M2 to Float
  Mx.SetMotors(Mx_M1+Mx_M2, 0);  // Set Motor Power to 0
  delay(1000);
  Mx.SetMode(Mx_M1, RESET);  // Reset M1
  Mx.SetMode(Mx_M2, RESET);  // Reset M2
}
// Increment Power to single motor
void inc_power(char motor, int increment){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power+increment); // Increment current power by set value
  delay(1000);
}
// Decrement Power to single motor
void dec_power(char motor, int decrement){
  Mx.SetMode(Mx_M1, FLOAT);  // Set M1 to Float
  Mx.SetMode(Mx_M2, FLOAT+INV);  // Set M2 to Float and Inverse motor direction
  Mx.SetMotors(motor, main_power-decrement); // Decrement current power by set value
  delay(1000);
}
// EOPD Object Detection
void EOPDsensor();{
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
