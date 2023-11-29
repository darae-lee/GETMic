from machine import Pin  # pragma: no cover
from machine import UserInteract  # pragma: no cover
import random  # pragma: no cover
def exec_code(random_interactions: list):  # pragma: no cover
    interactor = UserInteract()
    interactions_type_num = len(interactor.codes)
    space_num = 15
    interaction_gen = {}
    for idx in range(space_num):
        interaction_gen[idx] = 0
    
    buttonPin = 2
    ledPin = 13
    
    buttonPushCounter = 0
    buttonState = 0
    lastButtonState = 0
    
    p1 = Pin(ledPin, Pin.OUT)
    p2 = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    
    for interaction in random_interactions:
        timing_of_interaction = random.randint(0, space_num + 1)
        interaction_gen[timing_of_interaction] = interaction % interactions_type_num
        interactor.interact(interaction_gen[0])
        buttonState = p2.value()
        interactor.interact(interaction_gen[1])
        if buttonState != lastButtonState:
            interactor.interact(interaction_gen[2])
            if buttonState == 1:
                interactor.interact(interaction_gen[3])
                buttonPushCounter += 1
                interactor.interact(interaction_gen[4])
                print("on")
                interactor.interact(interaction_gen[5])
                print("number of button pushes: ", end="")
                interactor.interact(interaction_gen[6])
                print(buttonPushCounter)
                interactor.interact(interaction_gen[7])
            else:
                interactor.interact(interaction_gen[8])
                print("off")
                interactor.interact(interaction_gen[9])
        lastButtonState = buttonState
        interactor.interact(interaction_gen[10])
        if buttonPushCounter % 4 == 0:
            interactor.interact(interaction_gen[11])
            p1.value(1)
            interactor.interact(interaction_gen[12])
        else:
            interactor.interact(interaction_gen[13])
            p1.value(0)
            interactor.interact(interaction_gen[14])
        interaction_gen[timing_of_interaction] = 0
