import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
import machine  # pragma: no cover
import utime  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    analogPin = 0  # pragma: no cover
    sensorMin = 0  # pragma: no cover
    sensorMax = 600  # pragma: no cover
    
    new_min = 0  # pragma: no cover
    new_max = 3  # pragma: no cover
    
    adc_pin = machine.Pin(analogPin)  # pragma: no cover
    adc = machine.ADC(adc_pin)  # pragma: no cover
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

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
        
        utime.sleep(2/1000)
        if not interactor.is_alive():
            break
