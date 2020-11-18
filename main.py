# importing libraries
import pygame as pg
import vehicle
import obstacle
import road
import numpy as np
import pandas as pd
import matplotlib as plt
import globalVariables as gV
from random import choice, randint

# initialise pygame
pg.init()
timer_font = pg.font.SysFont('Comic Sans MS', 30)
distance_font = pg.font.SysFont('Comic Sans MS', 10)
simDisplay = pg.display.set_mode(gV.displaySize)
pg.display.set_caption('Highways England Connected Vehicle Simulation Environment')
clock = pg.time.Clock()

gV.deltaTime = 1 / gV.fps

if gV.seed is None:
    gV.seed = randint(0, 100000)

np.random.seed(gV.seed)

# define functions here
def processData(crossingTimes, roadObject):
    avgTime = 0
    for t in crossingTimes:
        avgTime += t
    if len(crossingTimes) > 0:
        avgTime /= len(crossingTimes)

    totalVelocity = 0
    for vehicleObject in roadObject.vehicleArray:
        totalVelocity += vehicleObject.velocity

    if len(roadObject.vehicleArray) != 0:
        avgVelocity = totalVelocity / len(roadObject.vehicleArray)

    else:
        avgVelocity = 0

    print("\nStats\n--------------------------------------------------------------------------------------------------")
    print("Simulation was run for", gV.runTimer, "seconds")
    print("Seed is", gV.seed)
    print("Average time taken for 1 vehicle to cross road:", avgTime, "s")
    if avgTime != 0:
        print("Vehicles per second:", 1 / avgTime)

    print("Average velocity of each lane at end of simulation:", roadObject.laneFlowRates)
    print("Average velocity of all lanes at end of simulation:", avgVelocity)
    print("--------------------------------------------------------------------------------------------------")


# Main loop flag
simQuit = False

# Create Objects for simulation
roadObject = road.Road(pos=[0, (gV.displaySize[1] / 2) - gV.roadWidth / 2], laneCount=gV.laneCount,
                       laneWidth=gV.roadWidth, meanArrivalRate=gV.arrivalRate)

# Add obstacle
roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=(gV.displaySize[0] / gV.scale) / 1.6, lane=0))
roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=(gV.displaySize[0] / gV.scale) / 1.5, lane=1))
# print("Obstacle position is", roadObject.obstructionArray[0].x)
# Record the starting time of simulation
runningTime = 0
# Main loop
while not simQuit:
    clock.tick(gV.fps)
    gV.runTimer += gV.deltaTime
    simDisplay.fill(gV.white)
    roadObject.draw(simDisplay)

    # Event handling loop
    for event in pg.event.get():
        # If red cross pressed then quit main loop
        if event.type == pg.QUIT:
            processData(gV.vehicleCrossingTimes, roadObject)
            simQuit = True

        if event.type == pg.KEYDOWN:
            # Move random car left or right
            if len(roadObject.vehicleArray) >= 1:
                if event.key == pg.K_LEFT:
                    choice(roadObject.vehicleArray).safeLaneChange(-1)

                if event.key == pg.K_RIGHT:
                    choice(roadObject.vehicleArray).safeLaneChange(1)

            # Add cars in specific lanes on number pressed
            if event.unicode.isnumeric() and int(event.unicode) < gV.laneCount:
                roadObject.spawnVehicle(lane=int(event.unicode))

    # generate traffic coming down road frequency dependent on poisson distribution
    if round(gV.runTimer, 1) % 1 == 0:
        roadObject.generateTraffic()

    # vehicle handling loop
    for vehicleObject in roadObject.vehicleArray:
        vehicleObject.checkHazards(roadObject, roadObject.vehicleArray, roadObject.obstructionArray)
        vehicleFinishTime = vehicleObject.move()

        if vehicleFinishTime is not None and vehicleFinishTime > 0:
            gV.vehicleCrossingTimes.append(vehicleFinishTime)

        vehicleObject.draw(simDisplay)

    # Recalculates the average velocity of all vehicles in each lane
    for laneNum in range(roadObject.laneCount):
        roadObject.calcLaneFlowRate(laneNum)

    # obstruction handling loop
    for obstacleObject in roadObject.obstructionArray:
        obstacleObject.draw(simDisplay)

    # 100 meter markers
    for i in range(0, int(gV.displaySize[0] / gV.scale), 100):
        surf = distance_font.render(str(i), False, gV.black)
        simDisplay.blit(surf, (i * gV.scale, 100))

    # Draw time to the display
    timer_surface = timer_font.render(str(round(gV.runTimer, 3)), False, gV.black)
    simDisplay.blit(timer_surface, (5, 0))

    pg.display.update()

pg.quit()
