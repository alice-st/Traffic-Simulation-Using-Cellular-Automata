import sys
import pygame
from pygame.locals import KEYDOWN, K_q
import numpy as np
import time
from create import create_world
from intersections import intersection
from metrics import check_if_congested, plot_congested, plot_flow
import matplotlib.pyplot as plt

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NUM_CARS = 100
MAX_SPEED = 4 #cells/step
TIMESTEPS = 100

# OUR GRID MAP:
cellMAP = np.zeros((50, 50))

_VARS = {'surf': False, 'gridWH': 400,
         'gridOrigin': (200, 100), 'gridCells': cellMAP.shape[0], 'lineWidth': 2}


def main():
    cycles = [5, 10, 15, 20]
    congested_dict = {}
    flow_dict = {}
    for cycle in cycles:
        world = create_world(cellMAP, NUM_CARS, MAX_SPEED, cycle)
        pygame.init()
        _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawSquareGrid(
         _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
        placeCells(world.traffic_map)
        pygame.display.update()
        congested_intersections = []
        for t in range(TIMESTEPS):
            checkEvents()
            _VARS['surf'].fill(GREY)
            drawSquareGrid(
             _VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
            world.update_map()
            congested_intersections.append(check_if_congested(world.traffic_map, world.intersections))
            time.sleep(1)
            if world.cars == []:
                break
            placeCells(world.traffic_map)
            pygame.display.update()
        congested_intersections = np.array(congested_intersections)
        congested_dict[cycle] = congested_intersections
        flow_dict[cycle] = world.flow
        # cycle += 2
        # if cycle == 11:
    plot_congested(congested_dict, TIMESTEPS)
    plot_flow(flow_dict, TIMESTEPS)
        #     break


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