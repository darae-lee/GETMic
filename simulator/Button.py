import machine
from machine import Pin
from machine import UserInteract
import utime

machine.load_board(__file__)
buttonPin = 2
ledPin = 13
buttonState = 0
p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)

interaction_seq = [(0, 1), (1, 0), (1, 1), (1, 0), (0, 1)]
interactor = UserInteract(interaction_seq)
interactor.start()

while True:
    buttonState = p2.value()
    print(buttonState)
    if buttonState == 1:
        p1.value(1)
        print("up")
    else:
        p1.value(0)
        print("down")
    utime.sleep(1)
    if not interactor.is_alive():
        break
    # input("wait")