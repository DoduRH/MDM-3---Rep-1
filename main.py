# importing libraries
import pygame as pg
import vehicle
import obstacle
import road
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

# Create Objects for simulation
vehicleArray = []
obstructionArray = [obstacle.Obstacle([gV.displaySize[0]/1.5, (gV.displaySize[1]/2)], (30, 40))]
roadObject = road.Road([0, (gV.displaySize[1]/2)-gV.roadWidth/2], 100, 1, gV.roadWidth, gV.arrivalRate)


def generateTraffic(road):
    for arrivals in range(0, np.random.poisson(road.meanArrivalRate)):
        vehicleArray.append(vehicle.Vehicle([-100, (gV.displaySize[1] / 2) - 10], (40, 20), [0, 0], [3, 0]))


# Main loop
while not simQuit:
    gV.deltaTime = clock.tick(gV.fps) / 1000
    gV.runTimer += gV.deltaTime
    simDisplay.fill(gV.white)
    roadObject.draw(simDisplay)

    # Event handling loop
    for event in pg.event.get():
        # If red cross pressed then quit main loop
        if event.type == pg.QUIT:
            simQuit = True

    # generate traffic coming down road frequency dependent on poisson distribution
    if round(gV.runTimer, 1) % 1 == 0:
        generateTraffic(roadObject)

    # vehicle handling loop
    for vehicleObject in vehicleArray:
        vehicleObject.checkHazards(roadObject, vehicleArray, obstructionArray)
        vehicleObject.move(roadObject)
        vehicleObject.draw(simDisplay)

    # obstruction handling loop
    for obstacleObject in obstructionArray:
        obstacleObject.draw(simDisplay)

    pg.display.update()

pg.quit()
quit()



