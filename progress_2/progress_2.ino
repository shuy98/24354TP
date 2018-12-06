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

/* global variables */
int forSpeed = 255;
int backSpeed = 255;

/* function prototypes */
void turnCCW();
void terminate();
void turnCW();
void moveForward();
void moveBackward();
void closeGripper();
void openGripper();

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz 
}

void loop() {
  if (Serial.available() > 0) { // signal detected from serial port
    char incomingByte = Serial.read();

    if (incomingByte == 'l') { // turn counter-clockwise
      turnCCW();

    } else if (incomingByte == 't') { // terminates
      terminate();

    } else if (incomingByte == 'r') { // turn clockwise
      turnCW();
      
    } else if (incomingByte == 'w') { // move forward
      moveForward();

    } else if (incomingByte == 's') { // move backward
      moveBackward();

    } else if (incomingByte == 'c') { // close gripper
      closeGripper();

    } else if (incomingByte == 'o') { // open gripper
      openGripper();

    } else { // unrecognized signal from Serial port
      Serial.println("unknown signal received");
    }
  }
}

void turnCCW() {
  backMotor->setSpeed(forSpeed);
  backMotor->run(FORWARD);
  
  leftMotor->setSpeed(forSpeed);
  leftMotor->run(FORWARD);
  
  rightMotor->setSpeed(forSpeed);
  rightMotor->run(FORWARD);
}

void terminate() {
  backMotor->run(RELEASE);
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
  gripper->run(RELEASE);
}

void turnCW() {
  backMotor->setSpeed(backSpeed);
  backMotor->run(BACKWARD);
  leftMotor->setSpeed(backSpeed);
  leftMotor->run(BACKWARD);
  rightMotor->setSpeed(backSpeed);
  rightMotor->run(BACKWARD);
}

void moveForward() {
  leftMotor->setSpeed(backSpeed);
  leftMotor->run(BACKWARD);
  rightMotor->setSpeed(forSpeed);
  rightMotor->run(FORWARD);
}

void moveBackward() {
  rightMotor->setSpeed(backSpeed);
  rightMotor->run(BACKWARD);
  leftMotor->setSpeed(forSpeed);
  leftMotor->run(FORWARD);
}

void closeGripper() {
  gripper->setSpeed(backSpeed);
  gripper->run(BACKWARD);
}

void openGripper() {
  gripper->setSpeed(forSpeed);
  gripper->run(FORWARD);
}