import machine  # pragma: no cover
from machine import UserInteract  # pragma: no cover
import random  # pragma: no cover
def exec_code(random_interactions: list):  # pragma: no cover
    interactor = UserInteract()
    interactions_type_num = len(interactor.codes)
    space_num = 7
    interaction_gen = {}
    for idx in range(space_num):
        interaction_gen[idx] = 0
    
    analogPin = 0
    ledPin = 13
    threshold = 400
    
    adc_pin = machine.Pin(analogPin)
    adc = machine.ADC(adc_pin)
    p1 = machine.Pin(ledPin, machine.Pin.OUT)
    
    
    for interaction in random_interactions:
        timing_of_interaction = random.randint(0, space_num + 1)
        interaction_gen[timing_of_interaction] = interaction % interactions_type_num
        interactor.interact(interaction_gen[0])
        analogValue = adc.read_u16()
        interactor.interact(interaction_gen[1])
        if analogValue > threshold:
            interactor.interact(interaction_gen[2])
            p1.value(1)
            interactor.interact(interaction_gen[3])
        else:
            interactor.interact(interaction_gen[4])
            p1.value(0)
            interactor.interact(interaction_gen[5])
        print(analogValue)
        interactor.interact(interaction_gen[6])
        interaction_gen[timing_of_interaction] = 0
