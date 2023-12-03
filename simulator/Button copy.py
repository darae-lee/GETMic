from machine import Pin
import utime

import threading
from machine import Interactor, load_board, HW_board

load_board(__file__)
interactor = Interactor()
t = threading.Thread(target=interactor, args=(HW_board, interaction_list))
first_iter_flag = True

buttonPin = 2
ledPin = 13
buttonState = 0

p1 = Pin(ledPin, Pin.OUT)
p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)

while True:
    buttonState = p2.value()
    
    if test_eq(buttonState, 1):
        p1.value(1)
    else:
        p1.value(0)
    utime.sleep(1)
    
    if first_iter_flag:
        t.start()
        first_iter_flag = False
        
        
        
        
        
        
        
def Interactor