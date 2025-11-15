class SwitchBoard:
    def __init__(self, default=None):
        switches = {1: False, 2: False, 3: False, 4: False, 5: False}
        self.switches = default if default is not None else switches

    def display_state(self):
        display = []
        for state in self.switches.values():
            if not state:
                display.append(0)
            else:
                display.append(1)
        print(display)

    def give_switches(self, switch_num):
        temp = (switch_num - 1, switch_num + 1)
        if all(i in self.switches.keys() for i in temp):
            return switch_num - 1, switch_num, switch_num + 1
        elif switch_num == 1:
            return 1, 2
        else:
            return 4, 5

    def change_state(self, switch_num):
        target_keys = self.give_switches(switch_num)
        for i in target_keys:
            self.switches[i] = not (self.switches[i])


switchBoard = SwitchBoard()

# For Second And Fourth Switch To Turn On
switchBoard.display_state()
switchBoard.change_state(1)
switchBoard.change_state(2)
switchBoard.change_state(3)
switchBoard.display_state()

