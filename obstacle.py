# Contains the obstacle class
import pygame as pg
import globalVariables as gV


class Obstacle:

    def __init__(self, road, x, lane, size):
        self.x = x
        self.lane = lane
        self.size = size
        self.road = road

    # Draws the obstacle to display
    def draw(self, display):
        pg.draw.rect(display, gV.red, [self.x, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05, self.size[0], self.size[1]])
