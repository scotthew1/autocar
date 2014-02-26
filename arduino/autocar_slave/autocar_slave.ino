#include <MatrixController.h>
#include <Wire.h>

long M1_cur, M2_cur, M1_val, M2_val;

void setup(){
  Serial.begin(9600);
  Mx.SetMode(Mx_M1, SLEW);
  Mx.SetMode(Mx_M2, SLEW);
}

ISR(TIMER1_COMPA_vect){
  Mx.MatrixController_ISR();
}

void loop(){
  CCW_90();
  delay(5000);
  CW_90();
  delay(5000);
  CCW_180();
  delay(5000);
}

void CCW_90(){  
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur + 415;
  M2_val = M2_cur + 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(2000);
}
void CW_90(){  
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur - 415;
  M2_val = M2_cur - 415;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(2000);
}
void CCW_180(){  
  M1_cur = Mx.MotorPosition(Mx_M1);
  delay(500);
  M2_cur = Mx.MotorPosition(Mx_M2);
  M1_val = M1_cur + 825;
  M2_val = M2_cur + 825;
  Mx.MotorTarget(Mx_M1, M1_val, 15);
  Mx.MotorTarget(Mx_M2, M2_val, 15);
  delay(2000);
}
