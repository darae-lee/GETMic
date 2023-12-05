import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
import machine  # pragma: no cover
import utime  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    analogPin = 0  # pragma: no cover
    ledPin = 13  # pragma: no cover
    threshold = 400  # pragma: no cover
    
    adc_pin = machine.Pin(analogPin)  # pragma: no cover
    adc = machine.ADC(adc_pin)  # pragma: no cover
    p1 = machine.Pin(ledPin, machine.Pin.OUT)  # pragma: no cover
    
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

    while True:
        analogValue = adc.read_u16()
        if analogValue > threshold:
            p1.value(1)
        else:
            p1.value(0)
        print(analogValue)
        utime.sleep(2/1000)
        if not interactor.is_alive():
            break
