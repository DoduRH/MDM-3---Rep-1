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
import globalVariables as gV


# initialise pygame
pg.init()
simDisplay = pg.display.set_mode(gV.displaySize)
clock = pg.time.Clock()

# Main loop flag
simQuit = False

car = vehicle.Vehicle([0, (gV.displaySize[1]/2)-10], (40, 20), [0, 0], [3, 0])
obstruction = obstacle.Obstacle([gV.displaySize[0]/2, (gV.displaySize[1]/2) - 20], (30, 40))
road = road.Road([0, (gV.displaySize[1]/2)-gV.roadWidth/2], 100, 1, gV.roadWidth)

# Main loop
while not simQuit:
    gV.deltaTime = clock.tick(gV.fps) / 1000

    # Main event loop
    for event in pg.event.get():
        # If red cross pressed then quit window
        if event.type == pg.QUIT:
            simQuit = True

    # vehicle handling loop
    car.checkHazards(road, obstruction)
    car.move(road)

    simDisplay.fill(gV.white)
    road.draw(simDisplay)
    car.draw(simDisplay)
    obstruction.draw(simDisplay)

    pg.display.update()

pg.quit()
quit()
