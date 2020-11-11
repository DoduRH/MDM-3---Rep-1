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
        self.meanArrivalRate = meanArrivalRate
        assert len(meanArrivalRate) == laneCount, "meanArrivalRate must have " + laneCount + " elements"

        self.vehicleArray = []
        self.obstructionArray = []
        self.currentCarIndex = -1
        self.font = pg.font.SysFont('Comic Sans MS', 30)

    def draw(self, display):
        for i in range(self.laneCount):
            pg.draw.rect(display, gV.grey, [self.pos[0], self.pos[1] + self.laneWidth * i * 1.05, gV.displaySize[0], self.laneWidth])

    def generateTraffic(self):
        for i in range(self.laneCount):
            for _ in range(0, np.random.poisson(self.meanArrivalRate[i])):
                self.vehicleArray.append(vehicle.Vehicle(road=self, size=(40, 30), lane=i, x=-40, speedlimit=np.random.normal(*gV.maxSpeedDist), velocity=0, acceleration=gV.acceleration, deceleration=gV.deceleration))

    # Returns list of cars in specified lane
    def carsInLane(self, lane):
        return [x for x in self.vehicleArray if x.lane == lane or x.oldLane == lane]

    def newCarIndex(self):
        self.currentCarIndex += 1
        return self.currentCarIndex