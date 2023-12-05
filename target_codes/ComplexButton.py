from machine import Pin
import utime

btn_pins = []
for i in range(3):
    pin = Pin(10+i, Pin.IN, Pin.PULL_DOWN)
    btn_pins.append(pin)

pins = [
    Pin(2, Pin.OUT),  # A
    Pin(3, Pin.OUT),  # B
    Pin(4, Pin.OUT),  # C
    Pin(5, Pin.OUT),  # D
    Pin(6, Pin.OUT),  # E
    Pin(8, Pin.OUT),  # F
    Pin(7, Pin.OUT),  # G
    Pin(0, Pin.OUT)   # DP (not connected)
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
]

def reset():
    """Turns off all segments on the 7-segment display."""
    for pin in pins:
        pin.value(1)

reset()


while True:
    bool_code = [pin.value() for pin in btn_pins] # 0 ~ 7
    number = int(''.join([str(i) for i in bool_code]), 2)
    if number == 0:
        for j in range(len(pins) - 1):
            pins[j].value(digits[0][j])
    elif number == 1:
        for j in range(len(pins) - 1):
            pins[j].value(digits[1][j])
    elif number == 2:
        for j in range(len(pins) - 1):
            pins[j].value(digits[2][j])
    elif number == 3:
        for j in range(len(pins) - 1):
            pins[j].value(digits[3][j])
    elif number == 4:
        for j in range(len(pins) - 1):
            pins[j].value(digits[4][j])
    elif number == 5:
        for j in range(len(pins) - 1):
            pins[j].value(digits[5][j])
    elif number == 6:
        for j in range(len(pins) - 1):
            pins[j].value(digits[6][j])
    elif number == 7:
        for j in range(len(pins) - 1):
            pins[j].value(digits[7][j])
    utime.sleep(1/1000)
    