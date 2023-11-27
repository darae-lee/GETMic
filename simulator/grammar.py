import itertools


class GrammarParser:
    def __init__(self, buttons=None, sensors=None):
        self.buttons = buttons
        self.sensors = sensors
        self.productions = self.generatate_productions()
        self.productions_length = len(self.productions)

    def generatate_productions(self) -> list:
        wait_expr = "# do_nothing"  # TODO
        productions = [wait_expr]

        if self.buttons is not None:
            bgp = ButtonGrammarParser(self.buttons)
            productions.extend(bgp.generate_expr())

        if self.sensors is not None:
            sgp = SensorGrammarParser(self.sensors)
            productions.extend(sgp.generate_expr())

        return productions

    def get_productions(self) -> list:
        return self.productions


class ButtonGrammarParser:
    def __init__(self, buttons: list):
        self.button_actions = ['pressButton', 'releaseButton']
        self.buttons = buttons

    def generate_expr(self) -> list:
        button_combinations = list(itertools.product(self.button_actions, self.buttons))
        expressions = [f'{action}({button})' for action, button in button_combinations]
        return expressions


class SensorGrammarParser:
    def __init__(self, sensors: list):
        self.sensor_actions = []
        self.sensors = sensors

    def generate_expr(self) -> list:
        button_combinations = list(itertools.product(self.sensor_actions, self.sensors))
        expressions = [f'{action}({button})' for action, button in button_combinations]
        return expressions
