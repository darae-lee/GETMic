from machine import Pin
import utime

buttonPin = 2
ledPin = 13
buttonState = 0

p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)

while True:
    buttonState = p2.value()
    
    if buttonState == 1:
        p1.value(1)
    else:
        p1.value(0)
    utime.sleep(1/1000)