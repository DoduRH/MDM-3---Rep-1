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
        pg.draw.rect(display, gV.blue, [self.pos[0]+(self.size[0]), self.pos[1],
                                       self.stoppingDistance, self.size[1]])

    # move vehicle up to max speed then stop
    def move(self, road):
        if 0 <= (self.velocity[0] + self.acceleration[0]) <= road.speedLimit:
            self.velocity[0] += self.acceleration[0]

        if 0 <= (self.velocity[1] + self.acceleration[1]) <= road.speedLimit:
            self.velocity[1] += self.acceleration[1]

        self.pos[1] += self.velocity[1] * gV.deltaTime
        self.pos[0] += self.velocity[0] * gV.deltaTime

    # checks that the vehicle's next movement is safe
    def checkHazards(self, road, vehiclesArray=None, obstaclesArray=None):
        # if there are no hazards within stopping distance then there is nothing to check as simulation is empty
        if (obstaclesArray and vehiclesArray) is None:
            return

        hazardFound = False

        # if an obstacle is within safe stopping distance then stop
        for obstacle in obstaclesArray:
            if (obstacle.pos[0] + obstacle.size[0] > (self.pos[0]+self.size[0])+self.stoppingDistance > obstacle.pos[0]
               and obstacle.pos[1] + obstacle.size[1] > (self.pos[1]+self.size[1]) > obstacle.pos[1]):
                hazardFound = True

        # if another vehicle is within safe stopping distance then stop
        for otherVehicle in vehiclesArray:
            # if the other vehicle is yourself then skip
            if self == otherVehicle:
                pass

            elif (otherVehicle.pos[0] + otherVehicle.size[0] >= (self.pos[0]+self.size[0])+self.stoppingDistance > otherVehicle.pos[0]
                  and otherVehicle.pos[1] + otherVehicle.size[1] >= (self.pos[1]+self.size[1]) > otherVehicle.pos[1]):
                hazardFound = True

        if hazardFound:
            self.acceleration = [-3, 0]

        else:
            self.acceleration = [3, 0]

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True
