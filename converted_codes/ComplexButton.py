import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
from machine import Pin  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    ledPin = 13  # pragma: no cover
    buttonState = 0  # pragma: no cover
    
    led = Pin(ledPin, Pin.OUT)  # pragma: no cover
    pins = []  # pragma: no cover
    for i in range(3):  # pragma: no cover
        pin = Pin(i, Pin.IN, Pin.PULL_DOWN)  # pragma: no cover
        pins.append(pin)  # pragma: no cover
    
    prev_number = -1  # pragma: no cover
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

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
        
        if not interactor.is_alive():
            break
