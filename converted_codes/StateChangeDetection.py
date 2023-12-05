import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
from machine import Pin  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)
    
    buttonPin = 2
    ledPin = 13
    
    buttonPushCounter = 0
    buttonState = 0
    lastButtonState = 0
    
    p1 = Pin(ledPin, Pin.OUT)
    p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

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
        if not interactor.is_alive():
            break
