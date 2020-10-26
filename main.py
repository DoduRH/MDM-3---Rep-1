# importing libraries
import pygame as pg
import vehicle
import obstacle
import road
import random
import time
import numpy as np
import pandas as pd
import matplotlib as plt
import globalVariables as gv


# initialise pygame
pg.init()
simDisplay = pg.display.set_mode(gv.displaySize)
clock = pg.time.Clock()

# Main loop flag
simQuit = False

car = vehicle.Vehicle([0, (gv.displaySize[1]/2)-10], (40, 20), [5, 0])
obstruction = obstacle.Obstacle([gv.displaySize[0]/2, (gv.displaySize[1]/2) - 20], (30, 40))
road = road.Road([0, (gv.displaySize[1]/2)-gv.roadWidth/2], 30, 1, gv.roadWidth)

# Main loop
while not simQuit:

    # Main event loop
    for event in pg.event.get():
        # If red cross pressed then quit window
        if event.type == pg.QUIT:
            simQuit = True

    car.move()
    simDisplay.fill(gv.white)
    road.draw(simDisplay)
    car.draw(simDisplay)
    obstruction.draw(simDisplay)

    pg.display.update()

    clock.tick(gv.fps)


pg.quit()
quit()
