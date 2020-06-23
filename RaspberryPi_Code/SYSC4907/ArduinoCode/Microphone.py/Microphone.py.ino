#include <Wire.h>
#include <stdio.h>

#define D6T_ID 0x0A
#define D6T_CMD 0x4C

int soundPin = 7;
int sensorValue;
int readBuffer[35];
float ptat;
float tdata[16];


void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  pinMode(soundPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  //sensorValue = analogRead(soundPin);
  
  //if(Serial.available()){
    //r = r * (Serial.read() - '0');
    //Serial.println(r);
  //}
  
  // D6T Thermal Sensor code

  // Asking for data
  
  Wire.beginTransmission(D6T_ID);
  Wire.write(D6T_CMD);
  Wire.endTransmission();
  
  // Getting sensor data
  Wire.requestFrom(D6T_ID,35);
  for(int i=0; i<35; i++) {
    readBuffer[i] = Wire.read();
  }
  ptat = (readBuffer[0]+(readBuffer[1]*256))*0.1; // Reference temp data

  // Temp Data
  for(int i=0; i<16; i++) {
    tdata[i] = (readBuffer[(i*2+2)]+(readBuffer[(i*2+3)]*256))*0.1;
  }
  
  // Display Temp
  float tempF;
  // Print ref temp
  if(tdata[0] > 0) { // check to see if there is data
    for(int i=0; i<16; i++) {
      tempF = tdata[i];

      Serial.print(tempF);
      Serial.print(',');
      
    }
    Serial.print(ptat);
    Serial.print(',');
    Serial.println();
    delay(30000);
    
  }

  //sensorValue = analogRead(soundPin);
  sensorValue = digitalRead(soundPin);

  if(sensorValue == 1){
    Serial.println("HIGH");
  }else{
    Serial.println("LOW");
  }
  delay(10000);
  
}
