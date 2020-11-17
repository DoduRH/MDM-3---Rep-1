# Contains the road class
import pygame as pg
import globalVariables as gV
import vehicle
import obstacle
import numpy as np


class Road:

    def __init__(self, pos, laneCount, laneWidth, meanArrivalRate):
        self.pos = pos
        self.laneCount = laneCount
        self.laneWidth = laneWidth
        self.laneFlowRates = np.zeros(laneCount)
        self.meanArrivalRate = meanArrivalRate
        assert len(meanArrivalRate) == laneCount, "meanArrivalRate must have " + laneCount + " elements"

        self.vehicleArray = []
        self.obstructionArray = []
        self.currentCarIndex = -1
        self.font = pg.font.SysFont('Comic Sans MS', round(laneWidth - laneWidth*0.25))

    def draw(self, display):
        for i in range(self.laneCount):
            pg.draw.rect(display, gV.grey, [self.pos[0], self.pos[1] + self.laneWidth * i * 1.05, gV.displaySize[0], self.laneWidth])

    def generateTraffic(self):
        for i in range(self.laneCount):
            for _ in range(0, np.random.poisson(self.meanArrivalRate[i])):
                randVehicleSizeSelector = np.random.randint(0, 3)
                randVehicleSize = gV.vehicleSizes[randVehicleSizeSelector]
                if randVehicleSizeSelector == 2:
                    gV.maxSpeedDist = (99.34212288, 9.934212288)
                else:
                    gV.maxSpeedDist = (137.77764, 9.934212288)
                if len(self.vehicleArray) == 0:
                    self.vehicleArray.append(
                        vehicle.Vehicle(road=self, vehicleLength=randVehicleSize, lane=i, x=-randVehicleSize,
                                        speedLimit=np.random.normal(*gV.maxSpeedDist),
                                        acceleration=gV.acceleration,
                                        deceleration=gV.deceleration))

                else:
                    # check for pre-existing cars within same lane to stop cars spawning on-top of each other
                    vehicleFound = False
                    for vehicleObject in self.carsInLane(i):
                        if vehicleObject.x < 100:
                            vehicleFound = True

                    if vehicleFound:
                        pass
                        # print("Error generating car car already in lane")

                    else:
                        self.vehicleArray.append(
                            vehicle.Vehicle(road=self, vehicleLength=randVehicleSize, lane=i, x=-randVehicleSize,
                                            speedLimit=np.random.normal(*gV.maxSpeedDist),
                                            acceleration=gV.acceleration,
                                            deceleration=gV.deceleration))

    # Returns list of cars in specified lane
    def carsInLane(self, lane):
        return [x for x in self.vehicleArray if x.lane == lane or x.oldLane == lane]

    def obstaclesInLane(self, lane):
        return [x for x in self.obstructionArray if x.lane == lane]

    # returns the average velocity of vehicles in a lane
    def calcLaneFlowRate(self, lane):
        vehiclesInLane = [x for x in self.vehicleArray if x.lane == lane or x.oldLane == lane]
        totalVelocity = 0
        for vehicleObject in vehiclesInLane:
            totalVelocity += vehicleObject.velocity

        if len(vehiclesInLane) != 0:
            avgVelocity = totalVelocity/len(vehiclesInLane)

        else:
            avgVelocity = 0

        self.laneFlowRates[lane] = avgVelocity

    def newCarIndex(self):
        self.currentCarIndex += 1
        return self.currentCarIndex
