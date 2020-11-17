# Contains the vehicle class
import pygame as pg
import numpy as np
import globalVariables as gV
import math


class Vehicle:

    # road (Road), size = (width, length) (tuple), lane (int), x (float), velocity = xVel (float), acceleration = xAcc (float)
    def __init__(self, road, vehicleLength, lane, x, speedLimit, acceleration, deceleration):
        self.road = road
        self.x = x
        self.size = (vehicleLength, road.laneWidth - road.laneWidth*0.25)
        self.lane = lane
        self.maxAcceleration = acceleration
        self.maxDeceleration = deceleration
        self.speedLimit = speedLimit
        self.velocity = self.speedLimit
        self.colour = [(self.speedLimit - self.velocity)/self.speedLimit * 200, self.velocity/self.speedLimit * 200, 0]
        self.crashed = False
        self.stoppingDistance = ((((1+(0.05*((((self.velocity/0.225)/1000)*(60**2))/1.6)))*((((self.velocity/0.225)/1000)*(60**2))/1.6))/3)*0.225)+(4*4.4444)
        self.changingLane = False
        self.oldLane = -1
        self.acceleration = 0
        self.changingProgress = 0
        self.changingTime = 50
        self.number = road.newCarIndex()
        self.timeAlive = 0

    # draws everything to do with vehicle
    def draw(self, display):
        # Draw car itself
        text = self.road.font.render(str(self.number), False, (0, 0, 0))
        if self.changingLane:
            y = self.road.laneWidth * 1.05 * self.oldLane + (self.lane - self.oldLane) * self.road.laneWidth * 1.05 * self.changingProgress/self.changingTime
            pg.draw.rect(display, self.colour, [self.x * gV.scale, self.road.pos[1] + 5 + y, self.size[0] * gV.scale, self.size[1]])
            display.blit(text, [self.x * gV.scale + self.size[0] * gV.scale/2 - text.get_rect().width/2, self.road.pos[1] - 2 + y])
            if self.changingProgress == self.changingTime:
                self.changingLane = False
                self.oldLane = self.lane
            else:
                self.changingProgress += 1
        else:
            pg.draw.rect(display, self.colour, [self.x * gV.scale, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 3, self.size[0] * gV.scale, self.size[1]])
            display.blit(text, [self.x * gV.scale + self.size[0] * gV.scale/2 - text.get_rect().width/2, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 - 2])
        # Visualise the vehicle's stopping distance
        # pg.draw.rect(display, gV.blue, [self.x+(self.size[0]), self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.stoppingDistance, self.size[1]])

    # move vehicle up to max speed then stop
    def move(self):
        self.stoppingDistance = ((((1+(0.05*((((self.velocity/0.225)/1000)*(60**2))/1.6)))*((((self.velocity/0.225)/1000)*(60**2))/1.6))/3)*0.225)+(4*4.4444)
        if (self.velocity + self.acceleration) <= self.speedLimit:
            self.velocity += self.acceleration * gV.deltaTime
            if self.velocity < 0:
                self.velocity = 0
            self.colour = [(self.speedLimit - self.velocity)/self.speedLimit * 200, self.velocity/self.speedLimit * 200, 0]

        self.x += self.velocity * gV.deltaTime
        self.timeAlive += gV.deltaTime

        if self.x > gV.displaySize[0] / gV.scale:
            self.road.vehicleArray.remove(self)
            # return finish time
            return self.timeAlive

        return

    # checks that the vehicle's next movement is safe
    def checkHazards(self, road, vehiclesArray=None, obstaclesArray=None):
        # if there are no hazards within stopping distance then there is nothing to check as simulation is empty
        if obstaclesArray is None and vehiclesArray is None:
            return

        hazardFound = False
        hazards = []

        # if an obstacle is within safe stopping distance then stop
        for obstacle in obstaclesArray:
            # Check it is in front, within 'range' and in same lane as self
            if self.x + self.size[0] < obstacle.x < self.x + self.size[0] + self.stoppingDistance and obstacle.lane == self.lane:
                hazardFound = True
                hazards.append(obstacle)

        # if another vehicle is within safe stopping distance then record hazard
        for otherVehicle in self.road.carsInLane(self.lane):
            # if the other vehicle is yourself then skip
            if self == otherVehicle:
                pass

            elif self.x < otherVehicle.x < self.x + self.size[0] + self.stoppingDistance:
                hazardFound = True
                hazards.append(otherVehicle)

        # If hazards are found then find the closest one and act accordingly
        if hazardFound:
            closestHazard = min(hazards, key=lambda k: k.x-self.x)
            hazardDistance = closestHazard.x - (self.x + self.size[0])
            if hazardDistance < self.stoppingDistance:
                if isinstance(closestHazard, Vehicle):
                    if self.velocity <= closestHazard.velocity:
                        self.acceleration = self.maxAcceleration
                    else:
                        # Break maximally for the closest 30% of the stopping distance
                        self.acceleration = self.maxDeceleration / (hazardDistance / (self.stoppingDistance * 0.3))
                        if self.acceleration <= self.maxDeceleration:
                            self.acceleration = self.maxDeceleration

                else:
                    # Break maximally for the closest 30% of the stopping distance
                    self.acceleration = self.maxDeceleration/(hazardDistance/(self.stoppingDistance*0.3))
                    if self.acceleration <= self.maxDeceleration:
                        self.acceleration = self.maxDeceleration

            changed = False
            # Try changing left and right
            changed = self.safeLaneChange(-1)
            if not changed:
                self.safeLaneChange(1)

        else:
            self.acceleration = self.maxAcceleration
            self.checkLaneFlowRates(road)

    # If the vehicle hits something then it has crashed and this function is called
    def crashed(self):
        self.crashed = True

    # Check for obstructions, then change lane.  Return True or false depending if the change was successful
    def safeLaneChange(self, direction):
        # Check is a valid lane
        targetLane = self.lane + direction
        if targetLane < 0 or targetLane >= self.road.laneCount:
            # self.log("Lane change failed - lack of lanes")
            return False

        # check if already in the process of changing lane
        if 0 < self.changingProgress < self.changingTime:
            # self.log("Lane change failed - currently changing lanes")
            return False

        # Check lane is not obstructed by another car
        newLaneTraffic = self.road.carsInLane(targetLane)
        for vehicleObject in newLaneTraffic:
            # Should take relative speed into account
            if (vehicleObject.x + vehicleObject.size[0] + vehicleObject.stoppingDistance < self.x or
               vehicleObject.x < self.x < vehicleObject.x + vehicleObject.size[0] or
               self.x < vehicleObject.x < self.x + self.size[0]):

                # self.log("lane change failed - car too close")
                return False

        newLaneObstacles = self.road.obstaclesInLane(targetLane)
        for obstacle in newLaneObstacles:
            if (math.isclose(obstacle.x, self.x + self.size[0], abs_tol=self.stoppingDistance) or
               obstacle.x < self.x < obstacle.x + obstacle.size[0] or
               self.x < obstacle.x < self.x + self.size[0]):

                # self.log("lane change failed - obstacle too close")
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

    # check the flow rates of all lanes. If one is higher than current lane change to lane with higher flow rate
    def checkLaneFlowRates(self, road):
        for lane in range(road.laneCount):
            if ((road.laneFlowRates[lane] > road.laneFlowRates[self.lane]) and
                    (len(road.carsInLane(lane)) < len(road.carsInLane(self.lane)))):

                if lane > self.lane:
                    self.safeLaneChange(1)

                else:
                    self.safeLaneChange(-1)

    # Log message including car colour (could swap for id or equivalent)
    def log(self, *message):
        print(self.number, *message)
