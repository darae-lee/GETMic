import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
import utime  # pragma: no cover
import machine  # pragma: no cover

def exec_code(random_interaction_seq: list):
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

    while True:
        sensorReading = adc.read_u16()
        local_range = int((sensorReading - sensorMin) * (new_max - new_min) / (sensorMax - sensorMin) + new_min)
    
        if local_range == 0:
            print("dark")
        elif local_range == 1:
            print("dim")
        elif local_range == 2:
            print("medium")
        elif local_range == 3:
            print("bright")
        
        utime.sleep(2)
        if not interactor.is_alive():
            break
