# Contains the road class
import pygame as pg
import globalVariables as gV
import vehicle
import obstacle
import numpy as np


class Road:

    def __init__(self, pos, speedLimit, laneCount, laneWidth, meanArrivalRate):
        self.pos = pos
        self.speedLimit = speedLimit
        self.laneCount = laneCount
        self.laneWidth = laneWidth
        self.meanArrivalRate = meanArrivalRate
        assert len(meanArrivalRate) == laneCount, "meanArrivalRate must have " + laneCount + " elements"

        self.vehicleArray = []
        self.obstructionArray = []

    def draw(self, display):
        for i in range(self.laneCount):
            pg.draw.rect(display, gV.grey, [self.pos[0], self.pos[1] + self.laneWidth * i * 1.05, gV.displaySize[0], self.laneWidth])

    def generateTraffic(self):
        for i in range(self.laneCount):
            for _ in range(0, np.random.poisson(self.meanArrivalRate[i])):
                self.vehicleArray.append(vehicle.Vehicle(road=self, size=(40, 30), lane=i, x=-40, velocity=0, acceleration=3))

    # Returns list of cars in specified lane
    def carsInLane(self, lane):
        return [x for x in self.vehicleArray if x.lane == lane or x.oldLane == lane]
