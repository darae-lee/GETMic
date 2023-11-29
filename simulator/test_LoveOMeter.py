import machine  # pragma: no cover
from machine import UserInteract  # pragma: no cover
import random  # pragma: no cover
def exec_code(random_interactions: list):  # pragma: no cover
    interactor = UserInteract()
    interactions_type_num = len(interactor.codes)
    space_num = 26
    interaction_gen = {}
    for idx in range(space_num):
        interaction_gen[idx] = 0
    
    sensorPin = 0
    baselineTemp = 20.0
    
    adc_pin = machine.Pin(sensorPin)
    adc = machine.ADC(adc_pin)
    
    pins = []
    for i in range(2, 5):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.value(0)
        pins.append(pin)
    
    for interaction in random_interactions:
        timing_of_interaction = random.randint(0, space_num + 1)
        interaction_gen[timing_of_interaction] = interaction % interactions_type_num
        interactor.interact(interaction_gen[0])
        sensorVal = adc.read_u16()
        interactor.interact(interaction_gen[1])
        print("Sensor Value: ", end="")
        interactor.interact(interaction_gen[2])
        print(sensorVal, end="")
        interactor.interact(interaction_gen[3])
        voltage = (sensorVal / 1024.0) * 5.0
        interactor.interact(interaction_gen[4])
        print(", Volts: ", end="")
        interactor.interact(interaction_gen[5])
        print(voltage, end="")
        interactor.interact(interaction_gen[6])
        print(", degree C: ", end="")
        interactor.interact(interaction_gen[7])
        temperature = (voltage - 0.5) * 100
        interactor.interact(interaction_gen[8])
        print(temperature)
        interactor.interact(interaction_gen[9])
        if (temperature < baselineTemp + 2):
            interactor.interact(interaction_gen[10])
            pins[0].value(0)
            interactor.interact(interaction_gen[11])
            pins[1].value(0)
            interactor.interact(interaction_gen[12])
            pins[2].value(0)
            interactor.interact(interaction_gen[13])
        elif temperature >= baselineTemp + 2 and temperature < baselineTemp + 4:
            interactor.interact(interaction_gen[14])
            pins[0].value(1)
            interactor.interact(interaction_gen[15])
            pins[1].value(0)
            interactor.interact(interaction_gen[16])
            pins[2].value(0)
            interactor.interact(interaction_gen[17])
        elif temperature >= baselineTemp + 4 and temperature < baselineTemp + 6:
            interactor.interact(interaction_gen[18])
            pins[0].value(1)
            interactor.interact(interaction_gen[19])
            pins[1].value(1)
            interactor.interact(interaction_gen[20])
            pins[2].value(0)
            interactor.interact(interaction_gen[21])
        elif temperature >= baselineTemp + 6:
            interactor.interact(interaction_gen[22])
            pins[0].value(1)
            interactor.interact(interaction_gen[23])
            pins[1].value(1)
            interactor.interact(interaction_gen[24])
            pins[2].value(1)
            interactor.interact(interaction_gen[25])
        interaction_gen[timing_of_interaction] = 0
