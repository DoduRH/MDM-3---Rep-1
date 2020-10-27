# Contains the road class
import pygame as pg
import globalVariables as gV


class Road:

    def __init__(self, pos, speedLimit, laneCount, laneWidth, meanArrivalRate):
        self.pos = pos
        self.speedLimit = speedLimit
        self.laneCount = laneCount
        self.laneWidth = laneWidth
        self.meanArrivalRate = meanArrivalRate

    def draw(self, display):
        for i in range(self.laneCount):
            pg.draw.rect(display, gV.grey, [self.pos[0], self.pos[1] + self.laneWidth * i * 1.05, gV.displaySize[0], self.laneWidth])
