import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import numpy as np
import random
from cars import car
from new_position import find_new_position
import time
from create import create_cars, create_traffic_map, create_intersections
from intersections import intersection

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NUM_CARS = 1
MAX_SPEED = 4 #cells/step

# OUR GRID MAP:
cellMAP = np.zeros((50, 50))

_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': cellMAP.shape[0], 'lineWidth': 2}


def main():
    traffic_map, cars, intersections, occupancy_map = build_map(cellMAP)
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    checkEvents()
    _VARS['surf'].fill(GREY)
    drawSquareGrid(
     _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
    placeCells(traffic_map)
    pygame.display.update()
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
         _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        traffic_map, cars, intersections, occupancy_map = update_map(traffic_map, cars, intersections, occupancy_map)
        time.sleep(0.5)
        if cars == []:
            break
        placeCells(traffic_map)
        pygame.display.update()


def update_map(traffic_map, cars, intersections, occupancy_map):
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
        c = update_car_state(c, traffic_map, intersections)

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
    return traffic_map, cars, intersections, occupancy_map


def update_car_state(car, traffic_map, intersections):

    if car.state == "NONE":
        car.update_state(random.randint(0, 1)) # 0:Non turning vehicle, 1: Turning Vehicle

    if car.state == "LEFT" or car.state == "RIGHT":
        print(car.state)
        return turning(car, traffic_map, intersections)
    else:
        print(car.state)
        return non_turning(car, traffic_map, intersections)


def turning(car, traffic_map, intersections):
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
    car = non_turning(car, traffic_map, intersections)
    return car


def non_turning(car, traffic_map, intersections):
    #Acceleration step
    if car.speed < MAX_SPEED:
        car.update_speed(car.speed+1)

    #Randomization step
    if car.speed > 0:
        if random.randint(0, 1) == 1:
            car.update_speed(car.speed-1)

    car = find_new_position(car, traffic_map, intersections)
    return car


def build_map(traffic_map):
    traffic_map = create_traffic_map(traffic_map)
    traffic_map, cars, occupancy_map = create_cars(traffic_map, NUM_CARS)
    intersections, traffic_map = create_intersections(traffic_map)

    return traffic_map, cars, intersections, occupancy_map


def placeCells(traffic_map):
    # GET CELL DIMENSIONS...
    cellBorder = 0
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    # DOUBLE LOOP
    for row in range(traffic_map.shape[0]):
        for column in range(traffic_map.shape[1]):
            # Is the grid cell tiled ?
            if(traffic_map[column][row] == -1): #OBSTACLES
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY, BLACK)
            elif (traffic_map[column][row] == 1): #OCCUPIED BY CARS
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY, BLUE)

            if (traffic_map[column][row] == 5): #GREEN_LIGHT_STATE
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY, GREEN)

            if (traffic_map[column][row] == 6): #RED LIGHT STATE
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY*row)
                    + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                    _VARS['gridOrigin'][1] + (celldimX*column)
                    + cellBorder + (2*column*cellBorder) + _VARS['lineWidth']/2,
                    celldimX, celldimY, RED)


# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY, color):
    pygame.draw.rect(
     _VARS['surf'], color,
     (x, y, dimX, dimY)
    )


def drawSquareGrid(origin, gridWH, cells):

    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin

    # DRAW Grid Border:
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
    # # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
    # # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (cont_x, cont_y),
      (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
    # # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
      (CONTAINER_WIDTH_HEIGHT + cont_x,
       CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

    # Get cell size, just one since its a square grid.
    cellSize = CONTAINER_WIDTH_HEIGHT/cells

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(cells):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (cont_x + (cellSize * x), cont_y),
           (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
    # # HORIZONTAl DIVISIONS
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (cont_x, cont_y + (cellSize*x)),
          (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()