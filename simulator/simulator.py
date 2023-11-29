import random
INPUT = 0
OUTPUT = 1
NON_SET = 2

class HWPin:
    def __init__(self, name="pin"):
        self.state = 0
        self.name = name
        self.connect = [] # it should contain component, not its pin except for the board pin...
        self.mode = NON_SET
    def __str__(self) -> str:
        return self.name
    def travel(self, state=-1, dir=OUTPUT):
        # print("I am PIN!", self.name)
        if state == -1:
            state = self.state
        else:
            self.state = state
        for con in self.connect:
            # call component except the board pin..?
            # if state != -1:
            # print(con)
            if isinstance(con, HWPin):
                # if next is pin, just update the next ones state
                if state != -1:
                    # print("update the connected one", state)
                    con.state = state
                        
            else:
                con.travel(self.state, dir)
            

class Board:
    def __init__(self, n=3):
        # input pins -> destination of flow
        # output pins -> starting point of flow
        self.pins = []
        for i in range(n):
            self.pins.append(HWPin(f"pin{i}"))
        # self.pin1 = HWPin("pin1")
        # self.pin2 = HWPin("pin2")
        self.gnd = HWPin("gnd")
        self.gnd.state = -1
        self.vcc = HWPin("vcc")
        self.vcc.state = 1
        self.grammar = []
        wait_expr = "do_nothing"
        self.grammar.append(wait_expr)
    
    def updategrammar(self, expressions):
        self.grammar.extend(expressions)
    
    def __str__(self) -> str:
        return "board"
    
    def pinmode(self, pin: int, mode: int):
        self.pins[pin].mode = mode # 0 for input 1 for output

    def digitalread(self, pin: int):
        return self.pins[pin].state

    def analogread(self, pin: int):
        return self.pins[pin].state
    
    def digitalwirte(self, pin: int, value: int):
        self.pins[pin].state = value
        self.updatecircuit()
        
    def userinteraction(self, code: int):
        code = code % len(self.grammar)
        if code != 0:
            # 0 for idle
            # print("call", code, self.grammar)
            # print(code)
            self.grammar[code]()
        self.updatecircuit()

    def updatecircuit(self):
        # starting from gnd?
        # starting from all output pins, propogate its state
        for pin in self.pins:
            if pin.mode == OUTPUT:
                # print("output", pin)
                # send travel????
                pin.travel(dir=OUTPUT)
                pass
            elif pin.mode == INPUT:
                # print("input", pin)
                # send travel in reverse way...?
                # for other, startin from the gnd direction (actually vcc)
                pass
        self.gnd.state = -1
        self.gnd.travel(dir=INPUT)
        self.gnd.state = -1
        # static one?
        pass
        
class Component:
    def __init__(self, left, right):
        self.left = HWPin("left")
        self.left.connect.append(left)
        left.connect.append(self)
        self.right = HWPin("right")
        self.right.connect.append(right)
        right.connect.append(self)
        self.state = 0
    
    def travel(self, state, dir):
        # print("HI!", dir, state, self.state)
        if state == -1:
            state = self.state
        else:
            self.state = state
        if dir == OUTPUT:
            # print("call left", self.state)
            self.left.travel(self.state, dir)
        else:
            # print("call right", self.state)
            self.right.travel(self.state, dir)
        # self.state = state
        
    
class LED(Component):
    def __init__(self, left, right):
        # assume left is - right is +
        super().__init__(left, right) 
    def __str__(self) -> str:
        return "LED with right {}".format(self.right)

class Button(Component):
    def __init__(self, left, right, board):
        super().__init__(left, right) 
        # if you push it, the state becomes high
        self.board = board
        self.updategrammar()

    def updategrammar(self):
        # self is a button, press and unpress in the relavent actions
        btn_combinations = [self.press, self.unpress]
        self.board.updategrammar(btn_combinations)
        # if push, high / unpush, low
    
    def press(self):
        self.state = 1 # update internal state

    def unpress(self):
        self.state = 0 # update internal state

    def __str__(self) -> str:
        return "BTN with right {}".format(self.right)


class AnalogComponent(Component):
    # analog input sensor
    def __init__(self, left, right, board):
        super().__init__(left, right) 
        # if you push it, the state becomes high
        self.board = board
        self.max_value = 1024
        self.state = random.randrange(0, self.max_value)
        self.updategrammar()

    def updategrammar(self):
        temp_combinations = [lambda x=value: self.setvalue(x) for value in range(self.max_value)]
        self.board.updategrammar(temp_combinations)
    
    def setvalue(self, value):
        self.state = value # update internal state

class TemperatureSensor(AnalogComponent):
    def __str__(self):
        return "Temperature sensor with right {}".format(self.right)
    
class Potentialmeter(AnalogComponent):
    def __str__(self) -> str:
        return "Potentialmeter sensor with right {}".format(self.right)

class Photoresistor(AnalogComponent):
    def __str__(self) -> str:
        return "Photoresistor sensor with right {}".format(self.right)

if __name__ == '__main__':
    print("currently assume one led with button, two pin in board")
    print("for led assume left is - right is +")
    print("use default setting with no-malfunctining componet")
    board = Board()
    led_right = int(input("LED right 0 or 1: "))
    led = LED(board.gnd, board.pins[led_right])
    btn_right = int(input("BTN right 0 or 1: "))
    btn = Button(board.gnd, board.pins[btn_right], board)

    board.pinmode(led_right, OUTPUT)
    board.pinmode(btn_right, INPUT)
    read_val = board.digitalread(btn_right)
    print(read_val)
    print(board.grammar)
    print("press!!")
    board.userinteraction(0)
    print(board.digitalread(btn_right))
    board.digitalwirte(led_right, 1)
    print(board.digitalread(btn_right))
    