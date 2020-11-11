# Contains the vehicle class
import pygame as pg
import numpy as np
import globalVariables as gV
import math
from random import randint


class Vehicle:

    # road (Road), size = (width, length) (tuple), lane (int), x (float), velocity = xVel (float), acceleration = xAcc (float)
    def __init__(self, road, size, lane, x, speedlimit, velocity, acceleration, deceleration):
        self.road = road
        self.x = x
        self.size = size
        self.lane = lane
        self.velocity = velocity
        self.maxAcceleration = acceleration
        self.maxDeceleration = deceleration
        self.speedLimit = speedlimit
        self.colour = (128, 128, 0)
        self.crashed = False
        self.stoppingDistance = 80
        self.changingLane = False
        self.oldLane = -1
        self.acceleration = 0
        self.number = road.newCarIndex()

    # draws everything to do with vehicle
    def draw(self, display):
        # Draw car itself
        text = self.road.font.render(str(self.number), False, (0, 0, 0))
        if self.changingLane:
            y = self.road.laneWidth * 1.05 * self.oldLane + (self.lane - self.oldLane) * self.road.laneWidth * 1.05 * self.changingProgress/self.changingTime
            pg.draw.rect(display, self.colour, [self.x, self.road.pos[1] + 5 + y, self.size[0], self.size[1]])
            display.blit(text, [self.x + self.size[0]/2 - text.get_rect().width/2, self.road.pos[1] - 2 + y])
            if self.changingProgress == self.changingTime:
                self.changingLane = False
                self.oldLane = self.lane
            else:
                self.changingProgress += 1
        else:
            pg.draw.rect(display, self.colour, [self.x, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.size[0], self.size[1]])
            # self.road.font.render_to(display, [self.x, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.size[0], self.size[1]], str(self.number))
            display.blit(text, [self.x + self.size[0]/2 - text.get_rect().width/2, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 - 2])
        # Visualise the vehicle's stopping distance
        # pg.draw.rect(display, gV.blue, [self.x+(self.size[0]), self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.stoppingDistance, self.size[1]])

    # move vehicle up to max speed then stop
    def move(self):
        if (self.velocity + self.acceleration) <= self.speedLimit:
            self.velocity += self.acceleration * gV.deltaTime
            if self.velocity < 0:
                self.velocity = 0
            self.colour = [(self.speedLimit - self.velocity)/self.speedLimit * 200, self.velocity/self.speedLimit * 200, 0]

        self.x += self.velocity * gV.deltaTime

        if self.x > gV.displaySize[0]:
            self.road.vehicleArray.remove(self)

    # checks that the vehicle's next movement is safe
    def checkHazards(self, road, vehiclesArray=None, obstaclesArray=None):
        # if there are no hazards within stopping distance then there is nothing to check as simulation is empty
        if obstaclesArray is None and vehiclesArray is None:
            return

        hazardFound = False
        hazards = []

        # if an obstacle is within safe stopping distance then stop
        for obstacle in obstaclesArray:
            if obstacle.x < self.x + self.size[0] + self.stoppingDistance and obstacle.lane == self.lane:
                hazardFound = True
                hazards.append(obstacle)

        # if another vehicle is within safe stopping distance then stop
        for otherVehicle in self.road.carsInLane(self.lane):
            # if the other vehicle is yourself then skip
            if self == otherVehicle:
                pass
            
            elif otherVehicle.x > self.x and self.x + self.size[0] + self.stoppingDistance > otherVehicle.x:
                hazardFound = True
                hazards.append(otherVehicle)

        if hazardFound:
            closestHazard = min(hazards, key=lambda k: k.x-self.x)
            hazardDistance = closestHazard.x - self.x
            if hazardDistance < 100:
                self.acceleration = self.maxDeceleration

            changed = False
            # Try changing left and right
            changed = self.safeLaneChange(-1)
            if not changed:
                changed = self.safeLaneChange(1)
            # Otherwise decelerate
            if not changed:
                self.acceleration = self.maxDeceleration

        else:
            self.acceleration = self.maxAcceleration

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True

    # Check for obstructions, then change lane.  Return True or false depending if the change was sucsessful
    def safeLaneChange(self, direction):
        # Check is a valid lane
        targetLane = self.lane + direction
        if targetLane < 0 or targetLane >= self.road.laneCount:
            # self.log("Lane change failed - lack of lanes")
            return False
        
        # Check lane is not obstructed by another car
        newLaneTraffic = self.road.carsInLane(targetLane)
        for car in newLaneTraffic:
            if math.isclose(car.x, self.x, abs_tol=120): # Should take relative speed into account
                # self.log("lane change failed - car too close")
                return False

        self.changeLane(direction)
        return True

    # Change lane - direction should be +- 1 to indicate which way to change
    def changeLane(self, direction):
        self.oldLane = self.lane
        self.lane += direction
        self.changingLane = True
        self.changingProgress = 0

        
        self.changingTime = 50

    # Log message including car colour (could swap for id or equivalent)
    def log(self, *message):
        print(self.colour, *message)