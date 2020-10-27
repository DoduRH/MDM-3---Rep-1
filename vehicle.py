# Contains the vehicle class
import pygame as pg
import numpy as np
import globalVariables as gV


class Vehicle:

    # startPos = [x, y] (array), size = (width, length) (tuple), velocity = [xVel, yVel] (array)
    def __init__(self, pos, size, velocity, acceleration):
        self.pos = np.array(pos)
        self.size = size
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)
        self.crashed = False
        self.stoppingDistance = 80

    # draws everything to do with vehicle
    def draw(self, display):
        # Draw car itself
        pg.draw.rect(display, gV.black, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
        # Visualise the vehicle's stopping distance
        pg.draw.rect(display, gV.blue, [self.pos[0]+(self.size[0]), self.pos[1]+(self.size[1]/2-1),
                                        self.stoppingDistance, 1])

    # move vehicle up to max speed then stop
    def move(self, road):
        if 0 <= (self.velocity[0] + self.acceleration[0]) <= road.speedLimit:
            self.velocity[0] += self.acceleration[0]

        if 0 <= (self.velocity[1] + self.acceleration[1]) <= road.speedLimit:
            self.velocity[1] += self.acceleration[1]

        self.pos[1] += self.velocity[1] * gV.deltaTime
        self.pos[0] += self.velocity[0] * gV.deltaTime

    # checks that the vehicle's next movement is safe
    def checkHazards(self, road, obstacles):
        # if the rect drawn in front of car intersects hazard then hazard is within stopping distance
        if obstacles.pos[0] + obstacles.size[0] > (self.pos[0]+self.size[0])+self.stoppingDistance > obstacles.pos[0]:
            self.acceleration = [-3, 0]

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True
