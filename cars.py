import random


class car(object):
    def __init__(self, initial_position, id):
        self.id = id
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.lane = self.set_initial_lane()
        self.speed = 0 #1 cell/step
        self.state = "NONE"
        self.light = "GREEN"

    def set_initial_lane(self):
        if self.position_x == 15:
            return 1
        elif self.position_x == 16:
            return 2
        elif self.position_x == 35:
            return 3
        elif self.position_x == 36:
            return 4
        elif self.position_y == 25:
            return 5
        elif self.position_y == 26:
            return 6
        elif self.position_y == 45:
            return 7
        else:
            return 8

    def update_speed(self, val):
        self.speed = val
        if self.speed < 0:
            self.speed = 0

    def update_state(self, state):
        if state == 2:
            self.state = "NONE"
        elif state == 0:
            self.state = "STRAIGHT"
        else:
            random_state = random.randint(0, 1)
            if random_state == 0:
                self.state = "LEFT"
            else:
                self.state = "RIGHT"

    def update_light(self, val):
        self.light = val

    def update_position(self, x, y):
        self.position_x = x
        self.position_y = y

    def update_lane(self, lane):
        self.lane = lane