import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
from machine import Pin  # pragma: no cover
from utime import sleep  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    # 7-segment display layout
    #       A
    #      ---
    #  F |  G  | B
    #      ---
    #  E |     | C
    #      ---
    #       D
    
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
        [0, 0, 0, 0, 0, 0, 0, 1], # 8  # pragma: no cover
        [0, 0, 0, 1, 1, 0, 0, 1], # 9  # pragma: no cover
        [0, 0, 0, 1, 0, 0, 0, 1], # a  # pragma: no cover
        [1, 1, 0, 0, 0, 0, 0, 1], # b  # pragma: no cover
        [0, 1, 1, 0, 0, 0, 1, 1], # C  # pragma: no cover
        [1, 0, 0, 0, 0, 1, 0, 1], # d  # pragma: no cover
        [0, 1, 1, 0, 0, 0, 0, 1], # E  # pragma: no cover
        [0, 1, 1, 1, 0, 0, 0, 1], # F  # pragma: no cover
    ]  # pragma: no cover
    
    def reset():  # pragma: no cover
        """Turns off all segments on the 7-segment display."""  # pragma: no cover
        for pin in pins:  # pragma: no cover
            pin.value(1)  # pragma: no cover
    
    reset()  # pragma: no cover
    
    switch = Pin(13, Pin.IN)  # pragma: no cover
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

    while True:
        if switch.value() == 1:
            # Ascending counter
            for i in range(len(digits)):
                if switch.value() == 0:
                    break
                for j in range(len(pins) - 1):
                    pins[j].value(digits[i][j])
                sleep(0.5)
        else:
            # Descending counter
            for i in range(len(digits) - 1, -1, -1):
                if switch.value() == 1:
                    break
                for j in range(len(pins)):
                    pins[j].value(digits[i][j])
                sleep(0.5)
        if not interactor.is_alive():  # pragma: no cover
            break
