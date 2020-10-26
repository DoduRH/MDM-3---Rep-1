# Contains the vehicle class
import pygame as pg
import globalVariables as gv


class Vehicle:

    # startPos = [x, y] (array), size = (width, length) (tuple), velocity = [xVel, yVel] (array)
    def __init__(self, pos, size, velocity):
        self.pos = pos
        self.size = size
        self.velocity = velocity
        self.crashed = False

    # draws rectangle at location of vehicle
    def draw(self, display):
        pg.draw.rect(display, gv.black, [self.pos[0], self.pos[1], self.size[0], self.size[1]])

    # move vehicle up to max speed then stop
    def move(self):
        if (self.pos[0] + self.velocity[0])-gv.displaySize[0] <= 30:
            self.pos[0] += self.velocity[0]

        if (self.pos[1] + self.velocity[1])-gv.displaySize[1] <= 30:
            self.pos[1] += self.velocity[1]

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True
