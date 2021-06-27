import random
from intersections import intersection
from cars import car
import numpy as np


def create_traffic_map(traffic_map):
    for row in range(traffic_map.shape[0]):
        for column in range(traffic_map.shape[1]):
            traffic_map[row, column] = -1

    traffic_map[15, :] = 0
    traffic_map[16, :] = 0
    traffic_map[35, :] = 0
    traffic_map[36, :] = 0
    traffic_map[:, 25] = 0
    traffic_map[:, 45] = 0
    traffic_map[:, 26] = 0
    traffic_map[:, 46] = 0

    return traffic_map


def create_cars(traffic_map, NUM_CARS):
    cars = []
    temp = 0
    occupancy_map = np.empty_like(traffic_map)

    while temp != NUM_CARS:
        rand_x = random.randint(0, traffic_map.shape[0]-1)
        rand_y = random.randint(0, traffic_map.shape[0]-1)
        if traffic_map[rand_x, rand_y] == 0:
            traffic_map[rand_x, rand_y] = 1
            cars.append(car((rand_x, rand_y), temp))
            occupancy_map[rand_x, rand_y] = cars[-1].id
            temp += 1

    return traffic_map, cars, occupancy_map


def create_intersections(traffic_map):

 # define intersections
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