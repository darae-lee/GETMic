import os
import sys
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(parent_dir, 'simulator'))
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list, clock_time: int):
    machine.load_board(__file__)
    
    analogPin = 0
    sensorMin = 0
    sensorMax = 600
    
    new_min = 0
    new_max = 3
    
    adc_pin = machine.Pin(analogPin)
    adc = machine.ADC(adc_pin)
    
    interactor = machine.UserInteract(random_interaction_seq)
    interactor.start()

    for i in range(clock_time):
        sensorReading = adc.read_u16()
        range = int((sensorReading - sensorMin) * (new_max - new_min) / (sensorMax - sensorMin) + new_min)
    
        if range == 0:
            print("dark")
        elif range == 1:
            print("dim")
        elif range == 2:
            print("medium")
        elif range == 3:
            print("bright")
        
        utime.sleep(2)
