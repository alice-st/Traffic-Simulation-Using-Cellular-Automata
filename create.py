import random
from intersections import intersection
from cars import car
import numpy as np
from new_position import find_new_position


class create_world():
    def __init__(self, cellMap, NUM_CARS, MAX_SPEED):
        self.MAX_SPEED = MAX_SPEED
        self.NUM_CARS = NUM_CARS
        self.traffic_map, self.cars, self.intersections = self.build_map(cellMap)

    def build_map(self, cellMap):
        traffic_map = self.create_traffic_map(cellMap)
        traffic_map, cars = self.create_cars(traffic_map)
        intersections, traffic_map = self.create_intersections(traffic_map)

        return traffic_map, cars, intersections

    def create_traffic_map(self, cellMap):
        for row in range(cellMap.shape[0]):
            for column in range(cellMap.shape[1]):
                cellMap[row, column] = -1

        cellMap[15, :] = 0
        cellMap[16, :] = 0
        cellMap[35, :] = 0
        cellMap[36, :] = 0
        cellMap[:, 25] = 0
        cellMap[:, 45] = 0
        cellMap[:, 26] = 0
        cellMap[:, 46] = 0

        return cellMap

    def create_cars(self, traffic_map):
        cars = []
        temp = 0

        while temp != self.NUM_CARS:
            rand_x = random.randint(0, traffic_map.shape[0]-1)
            rand_y = random.randint(0, traffic_map.shape[0]-1)
            if traffic_map[rand_x, rand_y] == 0:
                traffic_map[rand_x, rand_y] = 1
                cars.append(car((rand_x, rand_y)))
                temp += 1

        return traffic_map, cars

    def create_intersections(self, traffic_map):

        # Define intersections
        intersections = []

        intersections.append(intersection(15, (14, 25), "GREEN", (14, 24)))
        intersections.append(intersection(19, (14, 45), "GREEN", (14, 44)))
        intersections.append(intersection(35, (34, 25), "GREEN", (34, 24)))
        intersections.append(intersection(39, (34, 45), "GREEN", (34, 44)))

        intersections.append(intersection(67, (17, 26), "GREEN", (17, 27)))
        intersections.append(intersection(71, (17, 46), "GREEN", (17, 47)))
        intersections.append(intersection(89, (37, 26), "GREEN", (37, 27)))
        intersections.append(intersection(93, (37, 46), "GREEN", (37, 47)))

        intersections.append(intersection(16, (15, 27), "GREEN", (14, 27)))
        intersections.append(intersection(20, (15, 47), "GREEN", (14, 47)))
        intersections.append(intersection(36, (35, 27), "GREEN", (34, 27)))
        intersections.append(intersection(40, (35, 47), "GREEN", (34, 47)))

        intersections.append(intersection(66, (16, 24), "GREEN", (17, 24)))
        intersections.append(intersection(70, (16, 44), "GREEN", (17, 44)))
        intersections.append(intersection(86, (36, 24), "GREEN", (37, 24)))
        intersections.append(intersection(90, (36, 44), "GREEN", (37, 44)))

        for i in intersections:
            if i.state == "GREEN":
                traffic_map[i.visual_position_x, i.visual_position_y] = 5

        return intersections, traffic_map

    def update_map(self):
        new_list = self.cars.sort(key=lambda x: x.position_x)
        cars1 = []
        cars2 = []
        cars3 = []
        cars4 = []
        cars5 = []
        cars6 = []
        cars7 = []
        cars8 = []

        while(self.cars != []):
            if self.cars[0].position_x == 16:
                cars1.append(self.cars[0])
            elif self.cars[0].position_x == 36:
                cars2.append(self.cars[0])
            elif self.cars[0].position_x == 15:
                cars3.append(self.cars[0])
            elif self.cars[0].position_x == 35:
                cars4.append(self.cars[0])
            elif self.cars[0].position_y == 26:
                cars5.append(self.cars[0])
            elif self.cars[0].position_y == 46:
                cars6.append(self.cars[0])
            elif self.cars[0].position_y == 25:
                cars7.append(self.cars[0])
            elif self.cars[0].position_y == 45:
                cars8.append(self.cars[0])

            self.cars.pop(0)

        cars1.sort(key=lambda x: x.position_y, reverse=True)
        cars2.sort(key=lambda x: x.position_y, reverse=True)
        cars3.sort(key=lambda x: x.position_y)
        cars4.sort(key=lambda x: x.position_y)
        cars5.sort(key=lambda x: x.position_x)
        cars6.sort(key=lambda x: x.position_x)
        cars7.sort(key=lambda x: x.position_x, reverse=True)
        cars8.sort(key=lambda x: x.position_x, reverse=True)

        self.cars.extend(cars1)
        self.cars.extend(cars2)
        self.cars.extend(cars3)
        self.cars.extend(cars4)
        self.cars.extend(cars5)
        self.cars.extend(cars6)
        self.cars.extend(cars7)
        self.cars.extend(cars8)

        for c in self.cars:
            self.traffic_map[c.position_x, c.position_y] = 0
            c = self.update_car_state(c)
            previous_lane = c.lane

            if c.position_x == 0 and c.position_y == 0:
                self.cars.remove(c)
                if previous_lane == 1:
                    self.cars.append(car((15, 49)))
                    self.traffic_map[15, 49] = 1
                elif previous_lane == 2:
                    self.cars.append(car((16, 0)))
                    self.traffic_map[16, 0] = 1
                elif previous_lane == 3:
                    self.cars.append(car((35, 49)))
                    self.traffic_map[35, 49] = 1
                elif previous_lane == 4:
                    self.cars.append(car((36, 0)))
                    self.traffic_map[36, 0] = 1
                elif previous_lane == 5:
                    self.cars.append(car((0, 25)))
                    self.traffic_map[0, 25] = 1
                elif previous_lane == 6:
                    self.cars.append(car((49, 26)))
                    self.traffic_map[49, 26] = 1
                elif previous_lane == 7:
                    self.cars.append(car((0, 45)))
                    self.traffic_map[0, 45] = 1
                else:
                    self.cars.append(car((49, 46)))
                    self.traffic_map[49, 46] = 1
            else:
                self.traffic_map[c.position_x, c.position_y] = 1

    def update_car_state(self, car):

        if car.state == "NONE":
            car.update_state(random.randint(0, 1)) # 0:Non turning vehicle, 1: Turning Vehicle

        if car.state == "LEFT" or car.state == "RIGHT":
            # print(car.state)
            return self.turning(car)
        else:
            # print(car.state)
            return self.non_turning(car)

    def turning(self, car):
        for i in self.intersections:
            if car.position_x == i.position_x and car.position_y == i.position_y:
                # car is at intersection
                if car.light == "RED" and i.counter < 7:
                    i.update_counter(1)
                    i.update_light_state("RED")
                    self.traffic_map[i.visual_position_x, i.visual_position_y] = 6
                    return car # The vehicle does not move
                elif car.light == "RED" and i.counter >= 7:
                    i.update_counter(0)
                    i.update_light_state("GREEN")
                    car.update_light("GREEN")
                    self.traffic_map[i.visual_position_x, i.visual_position_y] = 5
                    return car
                else:
                    car = find_new_position(car, self.traffic_map, self.intersections)
                    car.update_state(random.randint(0, 1))
                    return car

        # Assume red light at intersection
        car.update_light("RED")
        car = self.non_turning(car)
        return car

    def non_turning(self, car):
        # Acceleration step
        if car.speed < self.MAX_SPEED:
            car.update_speed(car.speed+1)

        # Randomization step
        if car.speed > 0:
            if random.randint(0, 1) == 1:
                car.update_speed(car.speed-1)

        car = find_new_position(car, self.traffic_map, self.intersections)
        return car