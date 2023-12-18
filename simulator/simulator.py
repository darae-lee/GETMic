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
            if isinstance(con, HWPin):
                # if next is pin, just update the next ones state
                if state != -1:
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
        self.gnd = HWPin("gnd")
        self.gnd.state = 0
        self.vcc = HWPin("vcc")
        self.vcc.state = -1
        self.objects = []
        self.action_per_object = []
        self.readable_action_per_object = {}
        wait_expr = "do_nothing"
        self.objects.append(wait_expr)
        self.action_per_object.append([])
        self.readable_action_per_object[wait_expr] = []
    
    def updategrammar(self, object_key, actions, readable_actions):
        self.objects.append(object_key)
        self.action_per_object.append(actions)
        self.readable_action_per_object[object_key] = readable_actions
    
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
        
    def userinteraction(self, object_code: int, action_code: int):
        object_idx = object_code % len(self.objects)
        actions = self.action_per_object[object_idx]
        if len(actions) != 0:
            action_idx = action_code % len(actions)
            actions[action_idx]()
        self.updatecircuit()

    def convertreadable(self, object_code: int, action_code: int):
        object_idx = object_code % len(self.objects)
        actions = self.action_per_object[object_idx]
        object_name = list(self.readable_action_per_object.keys())[object_idx]
        action_name = "None"
        if len(actions) != 0:
            action_idx = action_code % len(actions)
            action_name = self.readable_action_per_object[object_name][action_idx]
        return object_name, action_name

    def updatecircuit(self):
        # starting from gnd?
        # starting from all output pins, propogate its state
        for pin in self.pins:
            if pin.mode == OUTPUT:
                pin.travel(dir=OUTPUT)
                pass
            elif pin.mode == INPUT:
                # for other, startin from the gnd direction (actually vcc)
                pass
        self.vcc.state = -1
        self.vcc.travel(dir=INPUT)
        self.vcc.state = -1
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
        self.name = str(right)
    
    def travel(self, state, dir):
        if state == -1:
            state = self.state
        else:
            self.state = state
        if dir == OUTPUT:
            self.left.travel(self.state, dir)
        else:
            self.right.travel(self.state, dir)
        
    
class LED(Component):
    def __init__(self, left, right):
        # assume left is - right is +
        super().__init__(left, right) 
    def __str__(self) -> str:
        return f"LED at {self.nae}"

class Button(Component):
    def __init__(self, left, right, board):
        super().__init__(left, right) 
        # if you push it, the state becomes high
        self.board = board
        self.updategrammar()

    def updategrammar(self):
        # self is a button, press and unpress in the relavent actions
        btn_combinations = [self.press, self.unpress]
        readable_combinations = ["press", "unpress"]
        self.board.updategrammar(str(self), btn_combinations, readable_combinations)
        # if push, high / unpush, low
    
    def press(self):
        self.state = 1 # update internal state

    def unpress(self):
        self.state = 0 # update internal state

    def __str__(self) -> str:
        return f"BTN at {self.name}"


class AnalogComponent(Component):
    # analog input sensor
    def __init__(self, left, right, board):
        super().__init__(left, right) 
        # if you push it, the state becomes high
        self.board = board
        self.max_value = 1024
        self.state = 0
        self.updategrammar()

    def updategrammar(self):
        temp_combinations = [lambda x=value: self.setvalue(x) for value in range(self.max_value)]
        readable_combinations = [f"set_value_{x}" for x in range(self.max_value)]
        self.board.updategrammar(str(self), temp_combinations, readable_combinations)
    
    def setvalue(self, value):
        self.state = value # update internal state

class TemperatureSensor(AnalogComponent):
    def __str__(self):
        return f"Temperature sensor at {self.name}"
    
class Potentiometer(AnalogComponent):
    def __str__(self) -> str:
        return f"Potentiometer sensor at {self.name}"

class Photoresistor(AnalogComponent):
    def __str__(self) -> str:
        return f"Photoresistor sensor at {self.name}"

if __name__ == '__main__':
    print("currently assume one led with button, two pin in board")
    print("for led assume left is - right is +")
    print("use default setting with no-malfunctining componet")
    board = Board()
    led_right = int(input("LED right 0 or 1: "))
    led = LED(board.gnd, board.pins[led_right])
    btn_right = int(input("BTN right 0 or 1: "))
    btn = Button(board.gnd, board.pins[btn_right], board)
    
