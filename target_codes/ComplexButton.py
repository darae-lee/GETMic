from machine import Pin
import utime

ledPin = 13
buttonState = 0

led = Pin(ledPin, Pin.OUT)
pins = []
for i in range(3):
    pin = Pin(i, Pin.IN, Pin.PULL_DOWN)
    pins.append(pin)

prev_number = -1

while True:
    bool_code = [pin.value() for pin in pins] # 0 ~ 7
    number = int(''.join([str(i) for i in bool_code]), 2)
    if number == 0:
        print("0", end=" ")
    elif number == 1:
        print("1", end=" ")
    elif number == 2:
        print("2", end=" ")
    elif number == 3:
        print("3", end=" ")
    elif number == 4:
        print("4", end=" ")
    elif number == 5:
        print("5", end=" ")
    elif number == 6:
        print("6", end=" ")
    elif number == 7:
        print("7", end=" ")
    utime.sleep(1/1000)
    
