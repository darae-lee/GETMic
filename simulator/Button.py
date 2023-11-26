from machine import Pin
from machine import UserInteract

buttonPin = 2
ledPin = 13
buttonState = 0
interactor = UserInteract()
codes = interactor.codes
print(codes)
p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
interactions = [0, 1, 2, 1, 0]
for interact in interactions:
    interactor.interact(interact)
    buttonState = p2.value()
    print(buttonState)
    if buttonState == 1:
        p1.value(1)
        print("up")
    else:
        p1.value(0)
        print("down")
    # utime.sleep(1)
    input("wait")