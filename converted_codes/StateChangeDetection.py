import os
import sys
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(parent_dir, 'simulator'))
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list, clock_time: int):
    machine.load_board(__file__)
    
    buttonPin = 2
    ledPin = 13
    
    buttonPushCounter = 0
    buttonState = 0
    lastButtonState = 0
    
    p1 = machine.Pin(ledPin, machine.Pin.OUT)
    p2 = machine.Pin(buttonPin, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

    for i in range(clock_time):
        buttonState = p2.value()
        if buttonState != lastButtonState:
            if buttonState == 1:
                buttonPushCounter += 1
                print("on")
                print("number of button pushes: ", end="")
                print(buttonPushCounter)
            else:
                print("off")
            utime.sleep(50)
        lastButtonState = buttonState
    
        if buttonPushCounter % 4 == 0:
            p1.value(1)
        else:
            p1.value(0)
        
        utime.sleep(1)
