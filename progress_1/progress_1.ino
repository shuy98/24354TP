#include <stdio.h>
#include <string.h>

int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(ledPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    //String turnOnLed = "turn on led";
    //String turnOffLed = "turn off led";
    //Serial.println(incomingString);

    if (incomingByte == 'o') {
      digitalWrite(ledPin, HIGH);     
      //delay(1000); 
    } else if (incomingByte == 'c'){
      digitalWrite(ledPin, LOW);      
    } else {
      for (int i=0; i<3; i++) {
        digitalWrite(ledPin, LOW);
        delay(500);
        digitalWrite(ledPin, HIGH);
        delay(500);
      }   
      digitalWrite(ledPin, LOW);   
    }
    
  }

}
