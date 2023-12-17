import os  # pragma: no cover
import sys  # pragma: no cover
parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # pragma: no cover
sys.path.append(os.path.join(parent_dir, 'simulator'))  # pragma: no cover
import machine  # pragma: no cover
import utime  # pragma: no cover

def exec_code(random_interaction_seq: list):
    machine.load_board(__file__)  # pragma: no cover
    
    sensorPin = 0  # pragma: no cover
    baselineTemp = 20.0  # pragma: no cover
    
    adc_pin = machine.Pin(sensorPin)  # pragma: no cover
    adc = machine.ADC(adc_pin)  # pragma: no cover
    
    pins = []  # pragma: no cover
    for i in range(2, 5):  # pragma: no cover
        pin = machine.Pin(i, machine.Pin.OUT)  # pragma: no cover
        pin.value(0)  # pragma: no cover
        pins.append(pin)  # pragma: no cover
    
    interactor = machine.UserInteract(random_interaction_seq)  # pragma: no cover
    interactor.start()  # pragma: no cover

    while True:
        sensorVal = adc.read_u16()
        print("Sensor Value: ", end="")
        print(sensorVal, end="")
    
        voltage = (sensorVal / 1024.0) * 5.0
    
        print(", Volts: ", end="")
        print(voltage, end="")
    
        print(", degree C: ", end="")
        temperature = (voltage - 0.5) * 100
        print(temperature)
    
        if (temperature < baselineTemp + 2):
            pins[0].value(0)
            pins[1].value(0)
            pins[2].value(0)
        elif temperature >= baselineTemp + 2 and temperature < baselineTemp + 4:
            pins[0].value(1)
            pins[1].value(0)
            pins[2].value(0)
        elif temperature >= baselineTemp + 4 and temperature < baselineTemp + 6:
            pins[0].value(1)
            pins[1].value(1)
            pins[2].value(0)
        elif temperature >= baselineTemp + 6:
            pins[0].value(1)
            pins[1].value(1)
            pins[2].value(1)
        utime.sleep(2/1000)
        if not interactor.is_alive():  # pragma: no cover
            break
