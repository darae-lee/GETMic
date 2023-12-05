import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)
    
    # 7-segment display layout
    #       A
    #      ---
    #  F |  G  | B
    #      ---
    #  E |     | C
    #      ---
    #       D
    
    pins = [
        machine.Pin(2, machine.Pin.OUT),  # A
        machine.Pin(3, machine.Pin.OUT),  # B
        machine.Pin(4, machine.Pin.OUT),  # C
        machine.Pin(5, machine.Pin.OUT),  # D
        machine.Pin(6, machine.Pin.OUT),  # E
        machine.Pin(8, machine.Pin.OUT),  # F
        machine.Pin(7, machine.Pin.OUT),  # G
        machine.Pin(0, machine.Pin.OUT)   # DP (not connected)
    ]
    
    # Common anode 7-segment display digit patterns
    digits = [
        [0, 0, 0, 0, 0, 0, 1, 1], # 0
        [1, 0, 0, 1, 1, 1, 1, 1], # 1
        [0, 0, 1, 0, 0, 1, 0, 1], # 2 
        [0, 0, 0, 0, 1, 1, 0, 1], # 3
        [1, 0, 0, 1, 1, 0, 0, 1], # 4
        [0, 1, 0, 0, 1, 0, 0, 1], # 5
        [0, 1, 0, 0, 0, 0, 0, 1], # 6
        [0, 0, 0, 1, 1, 1, 1, 1], # 7
        [0, 0, 0, 0, 0, 0, 0, 1], # 8
        [0, 0, 0, 1, 1, 0, 0, 1], # 9
        [0, 0, 0, 1, 0, 0, 0, 1], # a
        [1, 1, 0, 0, 0, 0, 0, 1], # b
        [0, 1, 1, 0, 0, 0, 1, 1], # C
        [1, 0, 0, 0, 0, 1, 0, 1], # d
        [0, 1, 1, 0, 0, 0, 0, 1], # E
        [0, 1, 1, 1, 0, 0, 0, 1], # F
    ]
    
    def reset():
        """Turns off all segments on the 7-segment display."""
        for pin in pins:
            pin.value(1)
    
    reset()
    
    switch = machine.Pin(13, machine.Pin.IN)
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

    while True:
        if switch.value() == 1:
            # Ascending counter
            for i in range(len(digits)):
                if switch.value() == 0:
                    break
                for j in range(len(pins) - 1):
                    pins[j].value(digits[i][j])
                utime.sleep(0.5)
        else:
            # Descending counter
            for i in range(len(digits) - 1, -1, -1):
                if switch.value() == 1:
                    break
                for j in range(len(pins)):
                    pins[j].value(digits[i][j])
                utime.sleep(0.5)
        if not interactor.is_alive():
            break
