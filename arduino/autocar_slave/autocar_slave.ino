#include <MatrixController.h>
#include <Wire.h>

long M1_cur, M2_cur, M1_val, M2_val;
int main_power;

void setup(){
  Serial.begin(9600);
}

ISR(TIMER1_COMPA_vect){
  Mx.MatrixController_ISR();
}

void loop(){
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

void CCW_90(){  
  Mx.SetMode(Mx_M1, SLEW);
  Mx.SetMode(Mx_M2, SLEW);
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur + 415;
  M2_val = M2_cur + 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);
  Mx.SetMode(Mx_M2, RESET);
}
void CW_90(){  
  Mx.SetMode(Mx_M1, SLEW);
  Mx.SetMode(Mx_M2, SLEW);
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur - 415;
  M2_val = M2_cur - 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);
  Mx.SetMode(Mx_M2, RESET);
}
void CCW_180(){  
  Mx.SetMode(Mx_M1, SLEW);
  Mx.SetMode(Mx_M2, SLEW);
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur + 825;
  M2_val = M2_cur + 825;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(3500);
  Mx.SetMode(Mx_M1, RESET);
  Mx.SetMode(Mx_M2, RESET);
}
void start_motors(int power){
  Mx.SetMode(Mx_M1, FLOAT);
  Mx.SetMode(Mx_M2, FLOAT+INV);
  main_power = power;
  Mx.SetMotors(Mx_M1+Mx_M2, 50);
}
void stop_motors(){
  Mx.SetMode(Mx_M1, FLOAT);
  Mx.SetMode(Mx_M2, FLOAT);
  Mx.SetMotors(Mx_M1+Mx_M2, 0);
  delay(1000);
  Mx.SetMode(Mx_M1, RESET);
  Mx.SetMode(Mx_M2, RESET);
}
void inc_power(char motor){
  Mx.SetMode(Mx_M1, FLOAT);
  Mx.SetMode(Mx_M2, FLOAT+INV);
  Mx.SetMotors(motor, main_power+5);
  delay(1000);
}
void dec_power(char motor){
  Mx.SetMode(Mx_M1, FLOAT);
  Mx.SetMode(Mx_M2, FLOAT+INV);
  Mx.SetMotors(motor, main_power-5);
  delay(1000);
}
