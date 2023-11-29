import simulator
import utime
import threading

HW_board = simulator.Board(n=14)

def load_board(path_name):
    global HW_board
    if "\\" in path_name:
        name = path_name.split("\\")[-1]
    else:
        name = path_name.split("/")[-1]
    # print(name)
    if name == "Button.py" or name == "StateChangeDetection.py":
        # Button.py
        led = simulator.LED(HW_board.gnd, HW_board.pins[13])
        btn = simulator.Button(HW_board.gnd, HW_board.pins[2], HW_board)
    elif name == "IfStatementConditional.py":
        # IfStatementConditional.py
        led = simulator.LED(HW_board.gnd, HW_board.pins[13])
        poten = simulator.Potentialmeter(HW_board.gnd, HW_board.pins[0], HW_board)
    elif name == "LoveOMeter.py":
        tem = simulator.TemperatureSensor(HW_board.gnd, HW_board.pins[0], HW_board)
        for i in range(2, 5):
            led = simulator.LED(HW_board.gnd, HW_board.pins[i])
    elif name == "SwitchCase.py":
        photo = simulator.Photoresistor(HW_board.gnd, HW_board.pins[0], HW_board)


class UserInteract(threading.Thread):
    def __init__(self, seq):
        threading.Thread.__init__(self)
        self.seq = seq
    def run(self):
        for o, a in self.seq:
            self.interact(o, a)
            utime.sleep(1)
        # print("done")
    def interact(self, object_code: int, action_code: int):
        HW_board.userinteraction(object_code, action_code)

class ADC:
    def __init__(self, pin):
        pin_number = pin.pin_number
        HW_board.pinmode(pin_number, simulator.INPUT)
        self.pin_number = pin_number
    
    def read_u16(self):
        return HW_board.analogread(self.pin_number)

class Pin:
    OUT = simulator.OUTPUT
    IN = simulator.INPUT
    PULL_DOWN = simulator.INPUT # as input
    def __init__(self, pin_number, mode=None, neglect=None):
        if mode != None:
            HW_board.pinmode(pin_number, mode)
        self.pin_number = pin_number
    def value(self, value=None):
        if value == None:
            # reading
            return HW_board.digitalread(self.pin_number)
        else:
            # writing
            return HW_board.digitalwirte(self.pin_number, value)

