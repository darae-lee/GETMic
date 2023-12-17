from machine import Pin
import utime

buttonPin = 2
masterButtonPin = 3
ledPin = 13

buttonPushCounter = 0
buttonState = 0
lastButtonState = 0
masterButtonState = 0

counter = 0

p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
p3 = Pin(masterButtonPin, Pin.IN, Pin.PULL_DOWN)

while True:
    buttonState = p2.value()
    masterButtonState = p3.value()
    if masterButtonState == 1:
        if buttonPushCounter == counter:
            counter += 1
            if counter == 1:
                print("reached 1!")
            elif counter == 2:
                print("reached 2!")
            elif counter == 3:
                print("reached 3!")
        buttonPushCounter = 0
    if buttonState != lastButtonState:
        if buttonState == 1:
            buttonPushCounter += 1
        utime.sleep(50/1000)
    lastButtonState = buttonState
    
    utime.sleep(1/1000)

