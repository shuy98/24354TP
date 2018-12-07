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
int forSpeed = 92;
int backSpeed = 92;
int gripperSpeed = 192;
int turnSpeed = 48;

/* function prototypes */
void turnCCW();
void terminate();
void turnCW();
void moveForward();
void moveBackward();
void closeGripper();
void openGripper();
void moveRight();
void moveLeft();

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

    } else if (incomingByte == 'd') { // move right
      moveRight();

    } else if (incomingByte == 'a') { // move left
      moveLeft();

    } else { // unrecognized signal from Serial port
      Serial.println("unknown signal received");
    }
  } 
}

void turnCCW() {
  backMotor->setSpeed(turnSpeed);
  backMotor->run(BACKWARD);
  
  leftMotor->setSpeed(turnSpeed);
  leftMotor->run(BACKWARD);
  
  rightMotor->setSpeed(turnSpeed);
  rightMotor->run(BACKWARD);
}

void terminate() {
  backMotor->run(RELEASE);
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
  gripper->run(RELEASE);
}

void turnCW() {
  backMotor->setSpeed(turnSpeed);
  backMotor->run(FORWARD);
  leftMotor->setSpeed(turnSpeed);
  leftMotor->run(FORWARD);
  rightMotor->setSpeed(turnSpeed);
  rightMotor->run(FORWARD);
}

void moveForward() {
  leftMotor->setSpeed(backSpeed);
  leftMotor->run(FORWARD);
  rightMotor->setSpeed(forSpeed);
  rightMotor->run(BACKWARD);
}

void moveBackward() {
  rightMotor->setSpeed(backSpeed);
  rightMotor->run(FORWARD);
  leftMotor->setSpeed(forSpeed);
  leftMotor->run(BACKWARD);
}

void moveRight() {
  rightMotor->setSpeed(forSpeed/2);
  rightMotor->run(FORWARD);
  leftMotor->setSpeed(forSpeed/2);
  leftMotor->run(FORWARD);

  backMotor->setSpeed(forSpeed/2*(3**0.5));
  backMotor->run(BACKWARD);  
}

void moveLeft() {
  rightMotor->setSpeed(backSpeed/2);
  rightMotor->run(BACKWARD);
  leftMotor->setSpeed(backSpeed/2);
  leftMotor->run(BACKWARD);

  backMotor->setSpeed(backSpeed/2*(3**0.5));
  backMotor->run(FORWARD);  
}

void closeGripper() {
  gripper->setSpeed(gripperSpeed);
  gripper->run(BACKWARD);
}

void openGripper() {
  gripper->setSpeed(gripperSpeed);
  gripper->run(FORWARD);
}
