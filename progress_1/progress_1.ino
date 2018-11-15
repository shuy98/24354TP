int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(ledPin, LOW);
}

void loop() {
  if (Serial.available() > 0) { // signal deteced from Serial port
    char incomingByte = Serial.read();

    if (incomingByte == 'o') {
      digitalWrite(ledPin, HIGH); 
    } else if (incomingByte == 'c'){
      digitalWrite(ledPin, LOW);      
    } else { // unrecognized signal from Serial port
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
