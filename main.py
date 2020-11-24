# importing libraries
import pygame as pg
import vehicle
import obstacle
import road
import numpy as np
import pandas as pd
import matplotlib as plt
import globalVariables as gV
from random import randint

# initialise pygame
pg.init()
timer_font = pg.font.SysFont('Comic Sans MS', 30)
distance_font = pg.font.SysFont('Comic Sans MS', 10)
simDisplay = pg.display.set_mode(gV.displaySize)
pg.display.set_caption('Highways England Connected Vehicle Simulation Environment')
clock = pg.time.Clock()

gV.deltaTime = 1 / gV.fps
# gV.fps = 1 / gV.deltaTime

if gV.seed is None:
    gV.seed = randint(0, 100000)

np.random.seed(gV.seed)


gV.avgVelocityTotal = []
gV.avgVelocityLanes = []

def averageVelocity(roadObject):
    '''
        Returns tupple containing total average velocity and average velocity of each lane
    '''
    velocities = [0 for _ in range(roadObject.laneCount)]
    carCount = [0 for _ in range(roadObject.laneCount)]

    for car in roadObject.vehicleArray:
        velocities[car.lane] += car.velocity
        carCount[car.lane] += 1

    totalVelocity = 0
    totalCount = 0
    laneVelocity = []
    for vel, count in zip(velocities, carCount):
        totalVelocity += vel
        totalCount += count
        if count == 0:
            laneVelocity.append("NaN")
        else:
            laneVelocity.append(vel/count)

    if totalCount == 0:
        avgVelocity = "NaN"
    else:
        avgVelocity = totalVelocity/totalCount

    return avgVelocity, laneVelocity

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

    if avgTime != 0:
        vps = 1/avgTime
    else:
        vps = "NaN"

    print("\nStats\n--------------------------------------------------------------------------------------------------")
    print("Simulation was run for", gV.runTimer, "seconds")
    print("Seed is", gV.seed)
    print("Average time taken for 1 vehicle to cross road:", avgTime, "s")
    print("Vehicles per second:", vps)

    print("Average velocity of each lane at end of simulation:", roadObject.laneFlowRates)
    print("Average velocity of all lanes at end of simulation:", avgVelocity)
    print("--------------------------------------------------------------------------------------------------")

    data = {
        "independantVariables": {
            "seed": gV.seed,
            "roadLength": gV.displaySize[0] * gV.scale,
            "deltaTime": gV.deltaTime,
            "laneCount": gV.laneCount,
            "arrivalRate": gV.arrivalRate,
            "acceleration": gV.acceleration,
            "deceleration": gV.deceleration,
            "maxSpeed": gV.maxSpeedDist,
            "vehicleSizes": gV.vehicleSizes
        },
        "runTimer": gV.runTimer,
        "avgerageTime": avgTime,
        "laneFlowRates": roadObject.laneFlowRates,
        "averageVelocityTotal": gV.avgVelocityTotal,
        "averageVelocityLanes": gV.avgVelocityLanes,
        "vehiclesPerSecond": vps,
        "vehicleFlowRate": gV.carCount
    }

    for key in data:
        if isinstance(data[key], np.ndarray):
            data[key] = data[key].tolist()
    return data


def visualiseSimulation(roadObject):
    clock.tick(gV.fps)
    simDisplay.fill(gV.white)
    roadObject.draw(simDisplay)

    # 100 meter markers
    for i in range(0, int(gV.displaySize[0] / gV.scale), 100):
        surf = distance_font.render(str(i), False, gV.black)
        simDisplay.blit(surf, (i * gV.scale, 100))

    # Draw time to the display
    timer_surface = timer_font.render(str(round(gV.runTimer, 3)), False, gV.black)
    simDisplay.blit(timer_surface, (5, 0))
    
    pg.display.update()

    simQuit = False
    # Event handling loop
    for event in pg.event.get():
        # If red cross pressed then quit main loop
        if event.type == pg.QUIT:
            simQuit = True

        if event.type == pg.KEYDOWN:
            # Move random car left or right
            if len(roadObject.vehicleArray) >= 1:
                if event.key == pg.K_LEFT:
                    np.random.choice(roadObject.vehicleArray).safeLaneChange(-1)

                if event.key == pg.K_RIGHT:
                    np.random.choice(roadObject.vehicleArray).safeLaneChange(1)

            # Add cars in specific lanes on number pressed
            if event.unicode.isnumeric() and int(event.unicode) < gV.laneCount:
                roadObject.spawnVehicle(lane=int(event.unicode))
    
    return simQuit


def resetSim():
    gV.seed = randint(0, 100000)
    np.random.seed(gV.seed)


def runSim(display=True, maxSimTime=None, seed=None):
    gV.carCount = []
    gV.avgVelocityTotal = []
    gV.avgVelocityLanes = []
    gV.tempCarCount = [0 for _ in range(gV.laneCount)]
    if seed is not None:
        gV.seed = seed
        np.random.seed(gV.seed)
    gV.runTimer = 0
    gV.vehicleCrossingTimes = []

    if maxSimTime is None:
        maxSimTime = 2 ** 31

    # Main loop flag
    simQuit = False

    # Create Objects for simulation
    roadObject = road.Road(pos=[0, (gV.displaySize[1] / 2) - gV.roadWidth / 2], laneCount=gV.laneCount,
                        laneWidth=gV.roadWidth, meanArrivalRate=gV.arrivalRate)

    # Add obstacle
    roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=2000, lane=0))
    # roadObject.obstructionArray.append(obstacle.Obstacle(road=roadObject, x=(gV.displaySize[0] / gV.scale) / 1.5, lane=1))
    # print("Obstacle position is", roadObject.obstructionArray[0].x)
    # Record the starting time of simulation
    # Main loop
    while not simQuit and gV.runTimer < maxSimTime:
        gV.runTimer += gV.deltaTime
        if display:
            simQuit = visualiseSimulation(roadObject)

        # generate traffic coming down road frequency dependent on poisson distribution
        if round(gV.runTimer, 1) % 1 == 0:
            roadObject.generateTraffic()

        if gV.runTimer % 60 < 0.1: # every 60 seconds
            gV.carCount.append(gV.tempCarCount)
            gV.tempCarCount = [0 for x in range(gV.laneCount)]

        # vehicle handling loop
        for vehicleObject in roadObject.vehicleArray:
            vehicleObject.checkHazards(roadObject, roadObject.vehicleArray, roadObject.obstructionArray)
            vehicleFinishTime = vehicleObject.move()

            if vehicleFinishTime is not None and vehicleFinishTime > 0:
                gV.vehicleCrossingTimes.append(vehicleFinishTime)

        # Recalculates the average velocity of all vehicles in each lane
        for laneNum in range(roadObject.laneCount):
            roadObject.calcLaneFlowRate(laneNum)
        
        velocities = averageVelocity(roadObject)
        
        gV.avgVelocityTotal.append(velocities[0])
        gV.avgVelocityLanes.append(velocities[1])
    
    return processData(gV.vehicleCrossingTimes, roadObject)

def stop():
    pg.quit()


if __name__ == "__main__":
    output = runSim(display=False, maxSimTime=120, seed=26697)
    stop()
