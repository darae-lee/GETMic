from simulator import *

if __name__ == '__main__':
    example_simulator = Simulator()
    button_1 = Button("Button 1")
    example_simulator.add_component(button_1)
    print(example_simulator.components)