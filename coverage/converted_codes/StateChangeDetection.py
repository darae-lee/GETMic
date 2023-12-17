import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
from machine import Pin  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    buttonPin = 2  # pragma: no cover
    ledPin = 13  # pragma: no cover
    
    buttonPushCounter = 0  # pragma: no cover
    buttonState = 0  # pragma: no cover
    lastButtonState = 0  # pragma: no cover
    
    p1 = Pin(ledPin, Pin.OUT)  # pragma: no cover
    p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)  # pragma: no cover
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

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
        if not interactor.is_alive():  # pragma: no cover
            break
