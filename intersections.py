class intersection():
    def __init__(self, id, position, state, visual_position):
        self.id = id
        self.position_x = position[0]
        self.position_y = position[1]
        self.state = state
        self.visual_position_x = visual_position[0]
        self.visual_position_y = visual_position[1]
        self.counter = 0

    def update_counter(self, val):
        if val == 0:
            self.counter = val
        else:
            self.counter += val

    def update_light_state(self, val):
        self.state = val
