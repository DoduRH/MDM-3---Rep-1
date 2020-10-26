# Contains the road class
import pygame as pg
import globalVariables as gv


class Road:

    def __init__(self, pos, speedLimit, laneCount, laneWidth):
        self.pos = pos
        self.speedLimit = speedLimit
        self.laneCount = laneCount
        self.laneWidth = laneWidth

    def draw(self, display):
        pg.draw.rect(display, gv.grey, [self.pos[0], self.pos[1], gv.displaySize[0], self.laneWidth])
