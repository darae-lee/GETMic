import machine  # pragma: no cover
from machine import UserInteract  # pragma: no cover
import random  # pragma: no cover
def exec_code(random_interactions: list):  # pragma: no cover
    interactor = UserInteract()
    interactions_type_num = len(interactor.codes)
    space_num = 11
    interaction_gen = {}
    for idx in range(space_num):
        interaction_gen[idx] = 0
    
    analogPin = 0
    sensorMin = 0
    sensorMax = 600
    
    new_min = 0
    new_max = 3
    
    adc_pin = machine.Pin(analogPin)
    adc = machine.ADC(adc_pin)
    
    for interaction in random_interactions:
        timing_of_interaction = random.randint(0, space_num + 1)
        interaction_gen[timing_of_interaction] = interaction % interactions_type_num
        interactor.interact(interaction_gen[0])
        sensorReading = adc.read_u16()
        interactor.interact(interaction_gen[1])
        range = int((sensorReading - sensorMin) * (new_max - new_min) / (sensorMax - sensorMin) + new_min)
        interactor.interact(interaction_gen[2])
        if range == 0:
            interactor.interact(interaction_gen[3])
            print("dark")
            interactor.interact(interaction_gen[4])
        elif range == 1:
            interactor.interact(interaction_gen[5])
            print("dim")
            interactor.interact(interaction_gen[6])
        elif range == 2:
            interactor.interact(interaction_gen[7])
            print("medium")
            interactor.interact(interaction_gen[8])
        elif range == 3:
            interactor.interact(interaction_gen[9])
            print("bright")
            interactor.interact(interaction_gen[10])
        interaction_gen[timing_of_interaction] = 0
