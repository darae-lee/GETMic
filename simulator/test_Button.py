from machine import Pin  # pragma: no cover
from machine import UserInteract  # pragma: no cover
import random  # pragma: no cover
def exec_code(random_interactions: list):  # pragma: no cover
    interactor = UserInteract()
    interactions_type_num = len(interactor.codes)
    space_num = 6
    interaction_gen = {}
    for idx in range(space_num):
        interaction_gen[idx] = 0
    
    buttonPin = 2
    ledPin = 13
    buttonState = 0
    
    p1 = Pin(ledPin, Pin.OUT)
    p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    
    for interaction in random_interactions:
        timing_of_interaction = random.randint(0, space_num + 1)
        interaction_gen[timing_of_interaction] = interaction % interactions_type_num
        interactor.interact(interaction_gen[0])
        buttonState = p2.value()
        interactor.interact(interaction_gen[1])
        if buttonState == 1:
            interactor.interact(interaction_gen[2])
            p1.value(1)
            interactor.interact(interaction_gen[3])
        else:
            interactor.interact(interaction_gen[4])
            p1.value(0)
            interactor.interact(interaction_gen[5])
        interaction_gen[timing_of_interaction] = 0
