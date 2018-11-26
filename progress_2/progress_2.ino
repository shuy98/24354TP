#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M4
Adafruit_DCMotor *myMotor = AFMS.getMotor(4);
// You can also make another motor on port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  myMotor->setSpeed(127);
  myMotor->run(FORWARD);
  // turn on motor
  myMotor->run(RELEASE);
}

void loop() {
  if (Serial.available() > 0) { // signal detected from serial port
    char incomingByte = Serial.read();

    if (incomingByte == 'o') {
      Serial.println("open signal received");
      myMotor->run(FORWARD);
    } else if (incomingByte == 'c'){
      Serial.println("close signal received");
      //myMotor->run(BACKWARD);
      myMotor->run(RELEASE);      
    } else if (incomingByte == 'b'){
      Serial.println("backward signal received");
      myMotor->run(BACKWARD);
      //myMotor->run(RELEASE);  
    } else { // unrecognized signal from Serial port
      Serial.println("unknown signal received");
      myMotor->run(RELEASE); 
    }
  }
}
