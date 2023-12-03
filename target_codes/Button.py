import machine
import utime

buttonPin = 2
ledPin = 13
buttonState = 0

p1 = machine.Pin(ledPin, machine.Pin.OUT)
p2 = machine.Pin(buttonPin, machine.Pin.IN, machine.Pin.PULL_DOWN)

while True:
    buttonState = p2.value()
    
    if buttonState == 1:
        p1.value(1)
    else:
        p1.value(0)
    utime.sleep(1)
