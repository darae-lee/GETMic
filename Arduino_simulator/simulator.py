    
class Board:
    def __init__(self, num_digital=14, num_analog=5) -> None:
        self.pins = []
        for i in range(num_digital):
            self.pins.append(BoardDigitalPin(f"D{str(i)}"))
        for i in range(num_analog):
            self.pins.append(BoardAnalogPin(f"A{str(i)}"))
        
        self.gnd = 0
        self.vcc = 0
    
class Component:
    def __init__(self, name="anonymous", suppliers=[], receivers=[]) -> None:
        self.name = name
        self.suppliers = suppliers
        self.receivers = receivers
        
class BoardDigitalPin(Component):
    def __init__(self, name) -> None:
        super.__init__(name)
        self.state = False

class BoardAnalogPin(Component):
    def __init__(self, name) -> None:
        super.__init__(name)
        self.value = 0
    
class LED(Component):
    def __init__(self, name, suppliers=[], receivers=[]) -> None:
        super.__init__(name, suppliers, receivers)
        self.on = False
    
class Button(Component):
    def __init__(self, name, suppliers=[], receivers=[]) -> None:
        super.__init__(name, suppliers, receivers)
        self.pressed = False
    
    def apply_interaction(self, interaction):
        self.pressed = interaction.interaction_type == "Press"
    
class TemperatureSensor(Component):
    def __init__(self, name, suppliers=[], receivers=[]) -> None:
        super.__init__(name, suppliers, receivers)
        self.temparature = None
    
    def apply_interaction(self, interaction):
        self.temparature = interaction.value
    
class Potentialmeter(Component):
    def __init__(self, name, suppliers=[], receivers=[]) -> None:
        super.__init__(name, suppliers, receivers)
        self.resistance = None
    
    def apply_interaction(self, interaction):
        self.resistance = interaction.value
    
class Photoresistor(Component):
    def __init__(self, name, suppliers=[], receivers=[]) -> None:
        super.__init__(name, suppliers, receivers)
        self.brightness = None
        
    def apply_interaction(self, interaction):
        self.brightness = interaction.value
 
class UserInteraction:
    def __init__(self, target, interaction_type, value=None):
        self.interaction_type = interaction_type
        self.target = target
        self.value = value
        
class Simulator:
    def __init__(self) -> None:
        self.source_code = ""
        self.board = Board()
        self.components = []
        # self.interaction_type = []
    
    def add_component(self, component):
        assert type(component) in [LED, Button, TemperatureSensor, Potentialmeter, Photoresistor], "Not supported component"
        self.components.append(component)
    
    def connect_component(self, component_name1, component_name2):
        component1 = None
        component2 = None
        for component in self.components:
            if component.name == component_name1:
                component1 = component
            elif component.name == component_name2:
                component2 = component
        for pin in self.board.pins:
            if pin.name == component_name1:
                component1 = pin
            elif pin.name == component_name2:
                component2 = pin
        if component1 is None or component2 is None:
            print("invalid connection")
            exit(0)
        
        component1.suppliers.append(component2)
        component1.receivers.append(component2)
        component2.supplier.append(component1)
        component2.receivers.append(component1)
        
    def digitalread(self, pin=None):
        return getattr(self.board, pin)
    
    def digitalwrite(self, pin=None, state=None):
        setattr(self.board, pin, state)
        self.updatestate()
        
    def userinteraction(self, user_interaction):
        target = None
        for component in self.components:
            if component.name == user_interaction.target:
                taget = component
                break
            
        if target is None:
            print(f"No component named {user_interaction.target}")
            exit(0)
        
        if not self.check_compatibility(target, user_interaction.interaction_type):
            print("Not compatible interaction")
            exit(0)
        
        target.apply_intertaction(user_interaction)
        self.updatestate()
    
    def check_compatibility(self, target, interaction_type):
        compatible = False
        if isinstance(target, Button):
            if interaction_type in ["Press", "Unpress"]:
                compatible = True
        else:
            if interaction_type == "SetTo":
                compatible = True
        return compatible
    
    def updatestate():
        pass