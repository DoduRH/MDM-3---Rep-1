# Contains the obstacle class
import pygame as pg
import globalVariables as gV


class Obstacle:

    def __init__(self, road, x, lane):
        self.x = x
        self.lane = lane
        self.road = road
        self.size = (40, self.road.laneWidth)

    # Draws the obstacle to display
    def draw(self, display):
        pg.draw.rect(display, gV.blue, [self.x * gV.scale, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05, self.size[0], self.size[1]])
