# Contains the vehicle class
import pygame as pg
import numpy as np
import globalVariables as gV


class Vehicle:

    # road (Road), size = (width, length) (tuple), lane (int), x (float), velocity = xVel (float), acceleration = xAcc (float)
    def __init__(self, road, size, lane, x, velocity, acceleration):
        self.road = road
        self.x = x
        self.size = size
        self.lane = lane
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)
        self.crashed = False
        self.stoppingDistance = 80

    # draws everything to do with vehicle
    def draw(self, display):
        # Draw car itself
        pg.draw.rect(display, gV.black, [self.x, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.size[0], self.size[1]])
        # Visualise the vehicle's stopping distance
        # pg.draw.rect(display, gV.blue, [self.x+(self.size[0]), self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.stoppingDistance, self.size[1]])

    # move vehicle up to max speed then stop
    def move(self):
        if 0 <= (self.velocity + self.acceleration) <= self.road.speedLimit:
            self.velocity += self.acceleration

        self.x += self.velocity * gV.deltaTime

        if self.x > gV.displaySize[0]:
            self.road.vehicleArray.remove(self)

    # checks that the vehicle's next movement is safe
    def checkHazards(self, road, vehiclesArray=None, obstaclesArray=None):
        # if there are no hazards within stopping distance then there is nothing to check as simulation is empty
        if (obstaclesArray and vehiclesArray) is None:
            return

        hazardFound = False

        # if an obstacle is within safe stopping distance then stop
        for obstacle in obstaclesArray:
            if (obstacle.x + obstacle.size[0] > (self.x+self.size[0])+self.stoppingDistance > obstacle.x
               and obstacle.lane == self.lane):
                hazardFound = True

        # if another vehicle is within safe stopping distance then stop
        for otherVehicle in vehiclesArray:
            # if the other vehicle is yourself then skip
            if self == otherVehicle:
                pass
            
            elif (otherVehicle.x > self.x and self.x + self.size[0] + self.stoppingDistance > otherVehicle.x 
                  and otherVehicle.lane == self.lane):
                hazardFound = True

        if hazardFound:
            self.acceleration = -3

        else:
            self.acceleration = 3

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True
