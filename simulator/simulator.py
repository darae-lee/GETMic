class Pin:
    def __init__(self, name="pin"):
        self.state = 0
        self.name = name
        self.connect = []
    def __str__(self) -> str:
        return self.name

class Board:
    def __init__(self):
        self.pin1 = Pin("pin1")
        self.pin2 = Pin("pin2")
        self.gnd = []
        self.vcc = Pin("vcc")
        self.vcc.state = 1
        
    def __str__(self) -> str:
        return "board"

    def digitalread(self, pin: int):
        if pin == 1:
            return self.pin1.state
        elif pin == 2:
            return self.pin2.state
    
    def digitalwirte(self, pin: int, value: int):
        if pin == 1:
            self.pin1.state = value
        elif pin == 2:
            self.pin2.state = value
        self.updatecircuit()
        
    def userinteraction(self, code):
        board.code[code]()
        self.updatecircuit()

    def updatecircuit(self):
        # starting from gnd?
        pass
        
class Component:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        # asume flow left to right
        # thus use left as its identifier, right to find next component
    
class LED(Component):
    def __init__(self, left, right):
        # assume left is - right is +
        super().__init__(left, right) 
    def __str__(self) -> str:
        return "LED with right {}".format(self.right)

class Button(Component):
    def __init__(self, left, right):
        super().__init__(left, right) 
        # if you push it, the state becomes high
    def press(self):
        self.right.state = 1
    def unpress(self):
        self.right.state = 0
    def __str__(self) -> str:
        return "BTN with right {}".format(self.right)

# class TemperatureSensor:
#     def __init__(self) -> None:
#         self.left
#         self.right
#     pass   
# class Potentialmeter:
#     def __init__(self) -> None:
#         self.left
#         self.right
#     pass   
# class Photoresistor:
#     def __init__(self) -> None:
#         self.left
#         self.right
#     pass    

if __name__ == '__main__':
    print("currently assume one led with button, two pin in board")
    print("for led assume left is - right is +")
    print("use default setting with no-malfunctining componet")
    board = Board()
    led_right = input("LED right 1 or 2: ")
    if led_right == "1":
        led = LED(board, board.pin1)
        board.gnd.append(led.left)
        board.pin1.connect.append(led)
    else:
        led = LED(board, board.pin2)
        board.gnd.append(led.left)
        board.pin2.connect.append(led)
    btn_right = input("BTN right 1 or 2: ")
    if btn_right == "1":
        btn = Button(board.gnd, board.pin1)
        board.gnd.append(btn.left)
        board.pin1.connect.append(btn)
    else:
        btn = Button(board.gnd, board.pin2)
        board.gnd.append(btn.left)
        board.pin2.connect.append(btn)
    board.code[0] = btn.unpress
    board.code[1] = btn.press
    
    print(board.pin1, board.pin2, board.gnd, board.vcc)
    print(led, btn)
    