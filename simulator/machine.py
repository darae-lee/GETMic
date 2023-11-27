import simulator

HW_board = simulator.Board(n=14)
led = simulator.LED(HW_board.gnd, HW_board.pins[13])
btn = simulator.Button(HW_board.gnd, HW_board.pins[2], HW_board)

class UserInteract:
    def __init__(self):
        self.codes = HW_board.codes
    def interact(self, code):
        HW_board.userinteraction(code)

class Pin:
    OUT = simulator.OUTPUT
    IN = simulator.INPUT
    PULL_DOWN = simulator.INPUT # as input
    def __init__(self, pin_number, mode, neglect=None):
        HW_board.pinmode(pin_number, mode)
        self.pin_number = pin_number
    def value(self, value=None):
        if value == None:
            # reading
            return HW_board.digitalread(self.pin_number)
        else:
            # writing
            return HW_board.digitalwirte(self.pin_number, value)

