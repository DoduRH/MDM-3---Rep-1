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
from random import choice


# initialise pygame
pg.init()
timer_font = pg.font.SysFont('Comic Sans MS', 30)
simDisplay = pg.display.set_mode(gV.displaySize)
pg.display.set_caption('Highways England Connected Vehicle Simulation Environment')
clock = pg.time.Clock()

gV.deltaTime = gV.fps/1000


# define functions here
def processData(crossingTimes, road):

    avgTime = 0
    for t in crossingTimes:
        avgTime += t
    if len(crossingTimes) > 0:
        avgTime /= len(crossingTimes)

    avgVelocity = 0
    for lane in range(road.laneCount):
        avgVelocity += road.laneFlowRates[lane]
    avgVelocity /= road.laneCount

    print("\nStats\n--------------------------------------------------------------------------------------------------")
    print("Average time taken for 1 vehicle to cross road:", avgTime, "s")
    if avgTime != 0:
        print("Vehicles per second:", 1/avgTime)

    print("Average velocity of each lane:", road.laneFlowRates)
    print("Average velocity of all lanes:", avgVelocity)
    print("--------------------------------------------------------------------------------------------------")


# checks if a car already exists in the lane where a vehicle spawn has been requested to spawn
# returns true if there is a car and false if it is safe to spawn car
def carSpawnCheck(vehicleSize):
    for vehicles in roadObject.vehicleArray:
        if vehicles.lane == int(event.unicode) and vehicles.x < 100:
            return True

    return False


# Main loop flag
simQuit = False

# Create Objects for simulation
roadObject = road.Road(pos=[0, (gV.displaySize[1]/2)-gV.roadWidth/2], laneCount=gV.laneCount, laneWidth=gV.roadWidth, meanArrivalRate=gV.arrivalRate)

# Add obstacle
roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=gV.displaySize[0]/1.5, lane=0))
# roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=gV.displaySize[0]/1.5, lane=1))

# Record the starting time of simulation
startTime = time.time()
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
                randVehicleSizeSelector = np.random.randint(0, 3)
                if randVehicleSizeSelector == 2:
                    gV.maxSpeedDist = (99.34212288, 9.934212288)
                else:
                    gV.maxSpeedDist = (137.77764, 9.934212288)
                randVehicleSize = gV.vehicleSizes[randVehicleSizeSelector]
                if len(roadObject.vehicleArray) == 0:
                    roadObject.vehicleArray.append(
                        vehicle.Vehicle(road=roadObject, vehicleLength=randVehicleSize, lane=int(event.unicode), x=-randVehicleSize,
                                        speedLimit=np.random.normal(*gV.maxSpeedDist),
                                        acceleration=gV.acceleration,
                                        deceleration=gV.deceleration))

                else:
                    if carSpawnCheck(randVehicleSize):
                        pass
                        # print("Error spawning car")
                    else:
                        roadObject.vehicleArray.append(
                            vehicle.Vehicle(road=roadObject, vehicleLength=randVehicleSize, lane=int(event.unicode), x=-randVehicleSize,
                                            speedLimit=np.random.normal(*gV.maxSpeedDist),
                                            acceleration=gV.acceleration,
                                            deceleration=gV.deceleration))

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

    # Draw time to the display
    timer_surface = timer_font.render(str(round(time.time() - startTime, 3)), False, gV.black)
    simDisplay.blit(timer_surface, (5, 0))

    pg.display.update()


pg.quit()
quit()
