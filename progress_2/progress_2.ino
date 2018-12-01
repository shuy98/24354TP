#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M4
Adafruit_DCMotor *backMotor = AFMS.getMotor(4); // back
// You can also make another motor on port M3
Adafruit_DCMotor *leftMotor = AFMS.getMotor(3); // left
Adafruit_DCMotor *rightMotor = AFMS.getMotor(1); // right
Adafruit_DCMotor *gripper = AFMS.getMotor(2); // gripper

int forSpeed = 255;
int backSpeed = 255;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  // backMotor->setSpeed(255);
  // leftMotor->setSpeed(255);
  // rightMotor->setSpeed(255);

  // backMotor->run(FORWARD);
  // // turn on motor
  // backMotor->run(RELEASE);

  // leftMotor->run(FORWARD);
  // // turn on motor
  // leftMotor->run(RELEASE);

  // rightMotor->run(FORWARD);
  // // turn on motor
  // rightMotor->run(RELEASE);  
}

void loop() {
  if (Serial.available() > 0) { // signal detected from serial port
    char incomingByte = Serial.read();

    if (incomingByte == 'l') {
      // Serial.println("forward signal received");
      
      backMotor->setSpeed(forSpeed);
      backMotor->run(FORWARD);
      
      leftMotor->setSpeed(forSpeed);
      leftMotor->run(FORWARD);
      
      rightMotor->setSpeed(forSpeed);
      rightMotor->run(FORWARD);

    } else if (incomingByte == 'c') {
      //Serial.println("close signal received");
      backMotor->run(RELEASE);
      leftMotor->run(RELEASE);
      rightMotor->run(RELEASE);
      //gripper->run(RELEASE);

    } else if (incomingByte == 'r') {
      //Serial.println("backward signal received");
      backMotor->setSpeed(backSpeed);
      backMotor->run(BACKWARD);
      leftMotor->setSpeed(backSpeed);
      leftMotor->run(BACKWARD);
      rightMotor->setSpeed(backSpeed);
      rightMotor->run(BACKWARD);
      
    } else if (incomingByte == 'w') {
      leftMotor->setSpeed(backSpeed);
      leftMotor->run(BACKWARD);
      rightMotor->setSpeed(forSpeed);
      rightMotor->run(FORWARD);

    } else if (incomingByte == 's') {
      rightMotor->setSpeed(backSpeed);
      rightMotor->run(BACKWARD);
      leftMotor->setSpeed(forSpeed);
      leftMotor->run(FORWARD);

    } else { // unrecognized signal from Serial port
      Serial.println("unknown signal received");
    }
  }
}
