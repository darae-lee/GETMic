from machine import Pin
import utime

buttonPin = 2
ledPin = 13

buttonPushCounter = 0
buttonState = 0
lastButtonState = 0

p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)

while True:
    buttonState = p2.value()
    if buttonState != lastButtonState:
        if buttonState == 1:
            buttonPushCounter += 1
            print("on")
            print("number of button pushes: ", end="")
            print(buttonPushCounter)
        else:
            print("off")
        utime.sleep(50/1000)
    lastButtonState = buttonState

    if buttonPushCounter % 4 == 0:
        p1.value(1)
    else:
        p1.value(0)
    
    utime.sleep(1/1000)
