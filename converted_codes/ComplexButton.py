import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
from machine import Pin  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    btn_pins = []  # pragma: no cover
    for i in range(3):  # pragma: no cover
        pin = Pin(10+i, Pin.IN, Pin.PULL_DOWN)  # pragma: no cover
        btn_pins.append(pin)  # pragma: no cover
    
    pins = [  # pragma: no cover
        Pin(2, Pin.OUT),  # A  # pragma: no cover
        Pin(3, Pin.OUT),  # B  # pragma: no cover
        Pin(4, Pin.OUT),  # C  # pragma: no cover
        Pin(5, Pin.OUT),  # D  # pragma: no cover
        Pin(6, Pin.OUT),  # E  # pragma: no cover
        Pin(8, Pin.OUT),  # F  # pragma: no cover
        Pin(7, Pin.OUT),  # G  # pragma: no cover
        Pin(0, Pin.OUT)   # DP (not connected)  # pragma: no cover
    ]  # pragma: no cover
    
    # Common anode 7-segment display digit patterns
    digits = [  # pragma: no cover
        [0, 0, 0, 0, 0, 0, 1, 1], # 0  # pragma: no cover
        [1, 0, 0, 1, 1, 1, 1, 1], # 1  # pragma: no cover
        [0, 0, 1, 0, 0, 1, 0, 1], # 2  # pragma: no cover
        [0, 0, 0, 0, 1, 1, 0, 1], # 3  # pragma: no cover
        [1, 0, 0, 1, 1, 0, 0, 1], # 4  # pragma: no cover
        [0, 1, 0, 0, 1, 0, 0, 1], # 5  # pragma: no cover
        [0, 1, 0, 0, 0, 0, 0, 1], # 6  # pragma: no cover
        [0, 0, 0, 1, 1, 1, 1, 1], # 7  # pragma: no cover
    ]  # pragma: no cover
    
    def reset():  # pragma: no cover
        """Turns off all segments on the 7-segment display."""  # pragma: no cover
        for pin in pins:  # pragma: no cover
            pin.value(1)  # pragma: no cover
    
    reset()  # pragma: no cover
    
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

    while True:
        bool_code = [pin.value() for pin in btn_pins] # 0 ~ 7
        number = int(''.join([str(i) for i in bool_code]), 2)
        if number == 0:
            print("0", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[0][j])
        elif number == 1:
            print("1", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[1][j])
        elif number == 2:
            print("2", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[2][j])
        elif number == 3:
            print("3", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[3][j])
        elif number == 4:
            print("4", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[4][j])
        elif number == 5:
            print("5", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[5][j])
        elif number == 6:
            print("6", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[6][j])
        elif number == 7:
            print("7", end=" ")
            for j in range(len(pins) - 1):
                pins[j].value(digits[7][j])
        utime.sleep(1/1000)
        
        if not interactor.is_alive():
            break
