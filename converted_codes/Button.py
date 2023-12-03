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
    buttonState = 0
    
    p1 = machine.Pin(ledPin, machine.Pin.OUT)
    p2 = machine.Pin(buttonPin, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

    for i in range(clock_time):
        buttonState = p2.value()
        
        if buttonState == 1:
            p1.value(1)
        else:
            p1.value(0)
        utime.sleep(1)
