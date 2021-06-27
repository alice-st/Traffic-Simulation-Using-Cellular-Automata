def find_new_position(car, traffic_map, intersections):
    if car.state == "STRAIGHT":
        car = continue_straight(car, traffic_map, intersections)
    elif car.state == "RIGHT":
        if is_intersection(car.position_x, car.position_y, traffic_map, intersections, car):
            car = turn_right(car, traffic_map, intersections)
        else:
            car = continue_straight(car, traffic_map, intersections)
    else:
        if is_intersection(car.position_x, car.position_y, traffic_map, intersections, car):
            car = turn_left(car, traffic_map, intersections)
        else:
            car = continue_straight(car, traffic_map, intersections)
    return car


def turn_left(car, traffic_map, intersections):
    if car.lane == 1 or car.lane == 3:
        if traffic_map[car.position_x, car.position_y-2] == 0 and traffic_map[car.position_x, car.position_y-1] == 0:
            if car.position_y == 27:
                car.update_lane(5)
                car.update_position(car.position_x, car.position_y-2)
                car.update_speed(2)
                (car.position_x, car.position_y-2)
            else:
                car.update_lane(7)
                car.update_position(car.position_x, car.position_y-2)
                car.update_speed(2)
                (car.position_x, car.position_y-2)
            car.update_state(2)
        else:
            return car
    elif car.lane == 2 or car.lane == 4:
        if traffic_map[car.position_x, car.position_y+2] == 0 and traffic_map[car.position_x, car.position_y+1] == 0:
            if car.position_y == 24:
                car.update_lane(6)
                car.update_position(car.position_x, car.position_y+2)
                car.update_speed(2)
                (car.position_x, car.position_y+2)
            else:
                car.update_lane(8)
                car.update_position(car.position_x, car.position_y+2)
                car.update_speed(2)
                (car.position_x, car.position_y+2)
            car.update_state(2)
        else:
            return car
    elif car.lane == 5 or car.lane == 7:
        if traffic_map[car.position_x+2, car.position_y] == 0 and traffic_map[car.position_x+1, car.position_y] == 0:
            if car.position_x == 14:
                car.update_lane(2)
                car.update_position(car.position_x+2, car.position_y)
                car.update_speed(2)
                (car.position_x+2, car.position_y)
            else:
                car.update_lane(4)
                car.update_position(car.position_x+2, car.position_y)
                car.update_speed(2)
                (car.position_x+2, car.position_y)
            car.update_state(2)
        else:
            return car
    else: #(if lane == 6 or 8)
        if traffic_map[car.position_x-2, car.position_y] == 0 and traffic_map[car.position_x-1, car.position_y] == 0:
            if car.position_x == 7:
                car.update_lane(1)
                car.update_position(car.position_x-2, car.position_y)
                car.update_speed(2)
                (car.position_x-2, car.position_y)
            else:
                car.update_lane(3)
                car.update_position(car.position_x-2, car.position_y)
                car.update_speed(2)
                (car.position_x-2, car.position_y)
            car.update_state(2)
        else:
            return car
    return car


def turn_right(car, traffic_map, intersections):
    if car.lane == 1 or car.lane == 3:
        if car.position_y == 27:
            car.update_lane(6)
            car.update_position(car.position_x, car.position_y-1)
            car.update_speed(1)
            (car.position_x, car.position_y-1)
        else:
            car.update_lane(8)
            car.update_position(car.position_x, car.position_y-1)
            car.update_speed(1)
            (car.position_x, car.position_y-1)
    elif car.lane == 2 or car.lane == 4:
        if car.position_y == 24:
            car.update_lane(5)
            car.update_position(car.position_x, car.position_y+1)
            car.update_speed(1)
            (car.position_x, car.position_y+1)
        else:
            car.update_lane(7)
            car.update_position(car.position_x, car.position_y+1)
            car.update_speed(1)
            (car.position_x, car.position_y+1)
    elif car.lane == 5 or car.lane == 7:
        if car.position_x == 4:
            car.update_lane(1)
            car.update_position(car.position_x+1, car.position_y)
            car.update_speed(1)
            (car.position_x+1, car.position_y)
        else:
            car.update_lane(3)
            car.update_position(car.position_x+1, car.position_y)
            car.update_speed(1)
            (car.position_x+1, car.position_y)
    else: #(if lane == 6 or 8)
        if car.position_x == 7:
            car.update_lane(2)
            car.update_position(car.position_x-1, car.position_y)
            car.update_speed(1)
            (car.position_x-1, car.position_y)
        else:
            car.update_lane(4)
            car.update_position(car.position_x-1, car.position_y)
            car.update_speed(1)
            (car.position_x-1, car.position_y)

    return car


def continue_straight(car, traffic_map, intersections):
    if car.lane == 1 or car.lane == 3:
        new_position_x, new_position_y, new_speed = right_to_left(car, traffic_map, intersections)
    elif car.lane == 2 or car.lane == 4:
        new_position_x, new_position_y, new_speed = left_to_right(car, traffic_map, intersections)
    elif car.lane == 5 or car.lane == 7:
        new_position_x, new_position_y, new_speed = top_to_bottom(car, traffic_map, intersections)
    elif car.lane == 6 or car.lane == 8:
        new_position_x, new_position_y, new_speed = bottom_to_top(car, traffic_map, intersections)

    car.update_position(new_position_x, new_position_y)
    car.update_speed(new_speed)

    return car


def right_to_left(car, traffic_map, intersections):
    current_speed = car.speed
    new_position_x = car.position_x
    new_position_y = car.position_y
    new_speed = car.speed

    if car.position_y-1 < 0:
        new_position_x = 0
        new_position_y = 0
        new_speed = 0
        return new_position_x, new_position_y, new_speed
    else:
        for i in range(1, current_speed+1):
            if car.position_y-i >= 0:
                if is_intersection(car.position_x, car.position_y-i, traffic_map, intersections, car):
                    if traffic_map[car.position_x, car.position_y-i] == 0:
                        new_position_x = car.position_x
                        new_position_y = car.position_y-i
                        new_speed = i
                        return new_position_x, new_position_y, new_speed
                    else:
                        break
                else:
                    if traffic_map[car.position_x, car.position_y-i] == 0:
                        new_position_x = car.position_x
                        new_position_y = car.position_y-i
                        new_speed = i
            else:
                break

    return new_position_x, new_position_y, new_speed


def left_to_right(car, traffic_map, intersections):
    current_speed = car.speed
    new_position_x = car.position_x
    new_position_y = car.position_y
    new_speed = car.speed
    if car.position_y+1 > traffic_map.shape[1]-1:
        new_position_x = 0
        new_position_y = 0
        new_speed = 0
        return new_position_x, new_position_y, new_speed
    else:
        for i in range(1, current_speed+1):
            if car.position_y+i <= traffic_map.shape[1]-1:
                if is_intersection(car.position_x, car.position_y+i, traffic_map, intersections, car):
                    if traffic_map[car.position_x, car.position_y+i] == 0:
                        new_position_x = car.position_x
                        new_position_y = car.position_y+i
                        new_speed = i
                        return new_position_x, new_position_y, new_speed
                    else:
                        break
                else:
                    if traffic_map[car.position_x, car.position_y+i] == 0:
                        new_position_x = car.position_x
                        new_position_y = car.position_y+i
                        new_speed = i
            else:
                break

    return new_position_x, new_position_y, new_speed


def top_to_bottom(car, traffic_map, intersections):
    current_speed = car.speed
    new_position_x = car.position_x
    new_position_y = car.position_y
    new_speed = car.speed

    if car.position_x+1 > traffic_map.shape[0]-1:
        new_position_x = 0
        new_position_y = 0
        new_speed = 0
        return new_position_x, new_position_y, new_speed
    else:
        for i in range(1, current_speed+1):
            if car.position_x+i <= traffic_map.shape[0]-1:
                if is_intersection(car.position_x+i, car.position_y, traffic_map, intersections, car):
                    if traffic_map[car.position_x+i, car.position_y] == 0:
                        new_position_x = car.position_x+i
                        new_position_y = car.position_y
                        new_speed = i
                        return new_position_x, new_position_y, new_speed
                    else:
                        break
                else:
                    if traffic_map[car.position_x+i, car.position_y] == 0:
                        new_position_x = car.position_x+i
                        new_position_y = car.position_y
                        new_speed = i
            else:
                break

    return new_position_x, new_position_y, new_speed


def bottom_to_top(car, traffic_map, intersections):
    current_speed = car.speed
    new_position_x = car.position_x
    new_position_y = car.position_y
    new_speed = car.speed
    if car.position_x-1 < 0:
        new_position_x = 0
        new_position_y = 0
        new_speed = 0
        return new_position_x, new_position_y, new_speed
    else:
        for i in range(1, current_speed+1):
            if car.position_x-i >= 0:
                if is_intersection(car.position_x-i, car.position_y, traffic_map, intersections, car):
                    if traffic_map[car.position_x-i, car.position_y] == 0:
                        new_position_x = car.position_x-i
                        new_position_y = car.position_y
                        new_speed = i
                        return new_position_x, new_position_y, new_speed
                    else:
                        break
                else:
                    if traffic_map[car.position_x-i, car.position_y] == 0:
                        new_position_x = car.position_x-i
                        new_position_y = car.position_y
                        new_speed = i
            else:
                break

    return new_position_x, new_position_y, new_speed


def is_intersection(x, y, traffic_map, intersections, car):
    for i in intersections:
        if x == i.position_x and y == i.position_y:
            return True
    return False