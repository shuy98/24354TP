import serial

uno = serial.Serial('COM10', 9600)

while True:
    userInput = input("Enter a character:")
    uno.write(userInput.encode())

