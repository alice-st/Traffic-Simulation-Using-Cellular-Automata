import random
from new_position import find_new_position
from cars import car


def update_map(traffic_map, cars, intersections, MAX_SPEED):
    new_list = cars.sort(key=lambda x: x.position_x)
    cars1 = []
    cars2 = []
    cars3 = []
    cars4 = []
    cars5 = []
    cars6 = []
    cars7 = []
    cars8 = []

    while(cars != []):
        if cars[0].position_x == 16:
            cars1.append(cars[0])
        elif cars[0].position_x == 36:
            cars2.append(cars[0])
        elif cars[0].position_x == 15:
            cars3.append(cars[0])
        elif cars[0].position_x == 35:
            cars4.append(cars[0])
        elif cars[0].position_y == 26:
            cars5.append(cars[0])
        elif cars[0].position_y == 46:
            cars6.append(cars[0])
        elif cars[0].position_y == 25:
            cars7.append(cars[0])
        elif cars[0].position_y == 45:
            cars8.append(cars[0])

        cars.pop(0)

    cars1.sort(key=lambda x: x.position_y, reverse=True)
    cars2.sort(key=lambda x: x.position_y, reverse=True)
    cars3.sort(key=lambda x: x.position_y)
    cars4.sort(key=lambda x: x.position_y)
    cars5.sort(key=lambda x: x.position_x)
    cars6.sort(key=lambda x: x.position_x)
    cars7.sort(key=lambda x: x.position_x, reverse=True)
    cars8.sort(key=lambda x: x.position_x, reverse=True)

    cars.extend(cars1)
    cars.extend(cars2)
    cars.extend(cars3)
    cars.extend(cars4)
    cars.extend(cars5)
    cars.extend(cars6)
    cars.extend(cars7)
    cars.extend(cars8)

    for c in cars:
        traffic_map[c.position_x, c.position_y] = 0
        c = update_car_state(c, traffic_map, intersections, MAX_SPEED)

        if c.position_x == 0 and c.position_y == 0:
            cars.remove(c)
            if traffic_map[16, 0] == 0:
                cars.append(car((16, 0), 2))
                traffic_map[16, 0] = 1
            elif(traffic_map[15, 49]) == 0:
                cars.append(car((15, 49), 2))
                traffic_map[15, 49] = 1
            elif(traffic_map[36, 0]) == 0:
                cars.append(car((36, 0), 2))
                traffic_map[36, 0] = 1
            elif (traffic_map[35, 49]) == 0:
                cars.append(car((35, 49), 2))
                traffic_map[35, 49] = 1
            elif (traffic_map[0, 25]) == 0:
                cars.append(car((0, 25), 2))
                traffic_map[0, 25] = 1
            elif (traffic_map[49, 26]) == 0:
                cars.append(car((49, 26), 2))
                traffic_map[49, 26] = 1
            elif (traffic_map[0, 45]) == 0:
                cars.append(car((0, 45), 2))
                traffic_map[0, 45] = 1
            elif (traffic_map[49, 46]) == 0:
                cars.append(car((49, 46), 2))
                traffic_map[49, 46] = 1
        else:
            traffic_map[c.position_x, c.position_y] = 1
    return traffic_map, cars, intersections


def update_car_state(car, traffic_map, intersections, MAX_SPEED):

    if car.state == "NONE":
        car.update_state(random.randint(0, 1)) # 0:Non turning vehicle, 1: Turning Vehicle

    if car.state == "LEFT" or car.state == "RIGHT":
        print(car.state)
        return turning(car, traffic_map, intersections, MAX_SPEED)
    else:
        print(car.state)
        return non_turning(car, traffic_map, intersections, MAX_SPEED)


def turning(car, traffic_map, intersections, MAX_SPEED):
    for i in intersections:
        if car.position_x == i.position_x and car.position_y == i.position_y:
            # car is at intersection
            if car.light == "RED" and i.counter < 7:
                i.update_counter(1)
                i.update_light_state("RED")
                traffic_map[i.visual_position_x, i.visual_position_y] = 6
                return car #the vehicle does not move
            elif car.light == "RED" and i.counter >= 7:
                i.update_counter(0)
                i.update_light_state("GREEN")
                car.update_light("GREEN")
                traffic_map[i.visual_position_x, i.visual_position_y] = 5
                return car
            else:
                car = find_new_position(car, traffic_map, intersections)
                car.update_state(random.randint(0, 1))
                return car

    #assume red light at intersection
    car.update_light("RED")
    car = non_turning(car, traffic_map, intersections, MAX_SPEED)
    return car


def non_turning(car, traffic_map, intersections, MAX_SPEED):
    #Acceleration step
    if car.speed < MAX_SPEED:
        car.update_speed(car.speed+1)

    #Randomization step
    if car.speed > 0:
        if random.randint(0, 1) == 1:
            car.update_speed(car.speed-1)

    car = find_new_position(car, traffic_map, intersections)
    return car