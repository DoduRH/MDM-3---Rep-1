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
from random import randint


# initialise pygame
pg.init()
simDisplay = pg.display.set_mode(gV.displaySize)
clock = pg.time.Clock()

# Main loop flag
simQuit = False

# Create Objects for simulation
roadObject = road.Road(pos=[0, (gV.displaySize[1]/2)-gV.roadWidth/2], speedLimit=100, laneCount=gV.laneCount, laneWidth=gV.roadWidth, meanArrivalRate=gV.arrivalRate)

# Add obstacle
roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=gV.displaySize[0]/1.5, lane=2, size=(30, 40)))

def generateTraffic(road):
    for arrivals in range(0, np.random.poisson(road.meanArrivalRate)):
        roadObject.vehicleArray.append(vehicle.Vehicle(road=roadObject, size=(40, 30), lane=randint(0, gV.laneCount-1), x=-100, velocity=0, acceleration=3))


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
    for vehicleObject in roadObject.vehicleArray:
        vehicleObject.checkHazards(roadObject, roadObject.vehicleArray, roadObject.obstructionArray)
        vehicleObject.move(roadObject)
        vehicleObject.draw(simDisplay)

    # obstruction handling loop
    for obstacleObject in roadObject.obstructionArray:
        obstacleObject.draw(simDisplay)

    pg.display.update()

pg.quit()
quit()
