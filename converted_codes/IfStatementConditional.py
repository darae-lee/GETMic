import os
import sys
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(parent_dir, 'simulator'))
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list, clock_time: int):
    machine.load_board(__file__)
    
    analogPin = 0
    ledPin = 13
    threshold = 400
    
    adc_pin = machine.Pin(analogPin)
    adc = machine.ADC(adc_pin)
    p1 = machine.Pin(ledPin, machine.Pin.OUT)
    
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

    for i in range(clock_time):
        analogValue = adc.read_u16()
        if analogValue > threshold:
            p1.value(1)
        else:
            p1.value(0)
        print(analogValue)
        utime.sleep(2)
