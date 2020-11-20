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
        self.size = (vehicleLength, road.laneWidth - road.laneWidth * 0.25)
        self.lane = lane
        self.maxAcceleration = acceleration
        self.maxDeceleration = deceleration
        self.speedLimit = speedLimit
        self.velocity = self.speedLimit
        self.colour = [(self.speedLimit - self.velocity) / self.speedLimit * 200, self.velocity / self.speedLimit * 200,
                       0]
        self.crashed = False
        self.stoppingDistance = ((1250/4101 + (125/8202 * self.velocity * 2.23694)) * (self.velocity * 2.23694)) + 3
        self.visionDistance = ((1250/4101 + (125/8202 * self.speedLimit * 2.23694)) * (self.speedLimit * 2.23694)) + 3
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
            y = self.road.laneWidth * 1.05 * self.oldLane + (
                    self.lane - self.oldLane) * self.road.laneWidth * 1.05 * self.changingProgress / self.changingTime
            pg.draw.rect(display, self.colour,
                         [self.x * gV.scale, self.road.pos[1] + 5 + y, self.size[0] * gV.scale, self.size[1]])
            display.blit(text, [self.x * gV.scale + self.size[0] * gV.scale / 2 - text.get_rect().width / 2,
                                self.road.pos[1] - 2 + y])
            if self.changingProgress == self.changingTime:
                self.changingLane = False
                self.oldLane = self.lane
            else:
                self.changingProgress += 1
        else:
            pg.draw.rect(display, self.colour,
                         [self.x * gV.scale, self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 3,
                          self.size[0] * gV.scale, self.size[1]])
            display.blit(text, [self.x * gV.scale + self.size[0] * gV.scale / 2 - text.get_rect().width / 2,
                                self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 - 2])
        # Visualise the vehicle's stopping distance
        # pg.draw.rect(display, gV.green, [(self.x * gV.scale + self.size[0] * gV.scale),self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + 5, self.visionDistance * gV.scale, self.size[1]])
        # pg.draw.rect(display, gV.blue, [(self.x*gV.scale+self.size[0] * gV.scale), self.road.pos[1] + self.road.laneWidth * self.lane * 1.05 + self.size[1] * 0.25, self.stoppingDistance * gV.scale, self.size[1] * 0.5])

    # move vehicle up to max speed then stop
    def move(self):
        self.stoppingDistance = ((1250/4101 + (125/8202 * self.velocity * 2.23694)) * (self.velocity * 2.23694)) + 3
        if (self.velocity + self.acceleration) <= self.speedLimit:
            self.velocity += self.acceleration * gV.deltaTime
            if self.velocity < 0:
                self.velocity = 0
            self.colour = [(self.speedLimit - self.velocity) / self.speedLimit * 200,
                           self.velocity / self.speedLimit * 200, 0]

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
            if self.x < obstacle.x < self.x + self.size[0] + self.visionDistance and obstacle.lane == self.lane:
                hazardFound = True
                hazards.append(obstacle)

        # if another vehicle is within safe stopping distance then record hazard
        for otherVehicle in self.road.carsInLane(self.lane):
            # if the other vehicle is yourself then skip
            if self == otherVehicle:
                pass

            elif self.x < otherVehicle.x < self.x + self.size[0] + self.visionDistance:
                hazardFound = True
                hazards.append(otherVehicle)

        # If hazards are found then find the closest one and act accordingly
        if hazardFound:
            closestHazard = min(hazards, key=lambda k: k.x - self.x)
            hazardDistance = closestHazard.x - (self.x + self.size[0])
            # self.log("hazard distance:", hazardDistance)
            if hazardDistance <= self.stoppingDistance:
                if isinstance(closestHazard, Vehicle):
                    # if the vehicle in front is traveling faster then accelerate to match speed
                    if self.velocity < closestHazard.velocity and self.x + self.size[0] + 14 < closestHazard.x:
                        self.acceleration = self.maxAcceleration

                    # if travelling faster than vehicle in front then try and overtake
                    elif self.velocity >= closestHazard.velocity and self.x + self.size[0] + 14 > closestHazard.x:
                        changed = self.safeLaneChange(1)
                        if not changed:
                            # Break maximally for the closest 30% of the stopping distance
                            self.acceleration = self.maxDeceleration / (hazardDistance / (self.stoppingDistance * 1))
                            if self.acceleration <= self.maxDeceleration:
                                self.acceleration = self.maxDeceleration

                    # if you need to break due to a vehicle start breaking and look to overtake using outside lane
                    else:
                        # Break maximally for the closest 30% of the stopping distance
                        self.acceleration = self.maxDeceleration / (hazardDistance / (self.stoppingDistance * 1))
                        if self.acceleration <= self.maxDeceleration:
                            self.acceleration = self.maxDeceleration

                else:
                    # Break maximally for the closest 30% of the stopping distance
                    self.acceleration = self.maxDeceleration / (hazardDistance / (self.stoppingDistance * 1))
                    if self.acceleration <= self.maxDeceleration:
                        self.acceleration = self.maxDeceleration

                    changed = self.safeLaneChange(1)
                    if not changed:
                        self.safeLaneChange(-1)

            # if hazard is outside of stopping distance it is not a true hazard so accelerate
            else:
                self.acceleration = self.maxAcceleration

        # else their are no hazards ahead so change to non-overtaking lane
        else:
            self.acceleration = self.maxAcceleration
            self.safeLaneChange(-1)
            # if self.checkLaneFlowRates(road):
            #    pass
            # else:
            #     self.safeLaneChange(-1)

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
            selfFrontBumper = self.x + self.size[0]
            selfBackBumper = self.x

            otherFrontBumper = vehicleObject.x + vehicleObject.size[0]
            otherBackBumper = vehicleObject.x

            # self front bumper
            if otherBackBumper < selfFrontBumper < otherFrontBumper:
                # self.log("vehicle", vehicleObject.number, "blocking self front bumper")
                return False

            # self back bumper
            if otherBackBumper < selfBackBumper < otherFrontBumper:
                # self.log("vehicle", vehicleObject.number, "blocking self back bumper")
                return False

            # other front bumper
            if selfBackBumper < otherFrontBumper < selfFrontBumper:
                # self.log("vehicle", vehicleObject.number, "blocking other front bumper")
                return False

            # other back bumper
            if selfBackBumper < otherBackBumper < selfFrontBumper:
                # self.log("vehicle", vehicleObject.number, "blocking other back bumper")
                return False

            # self stopping distance - other back bumper between self front bumper and self sopped distance
            if selfFrontBumper < otherBackBumper < selfFrontBumper + self.stoppingDistance and vehicleObject.velocity <= self.velocity:
                # self.log("vehicle", vehicleObject.number, "blocking self breaking distance")
                return False

            # self stopping distance
            if otherFrontBumper < selfBackBumper < otherFrontBumper + vehicleObject.stoppingDistance and vehicleObject.velocity >= self.velocity:
                # self.log("vehicle", vehicleObject.number, "blocking other breaking distance")
                return False

        newLaneObstacles = self.road.obstaclesInLane(targetLane)
        for obstacle in newLaneObstacles:
            if ((math.isclose(obstacle.x, self.x + self.size[0], abs_tol=self.stoppingDistance) and self.x < obstacle.x) or
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
        changed = False
        for lane in range(road.laneCount):
            if road.laneFlowRates[lane] > road.laneFlowRates[self.lane]:
                if lane > self.lane:
                    changed = self.safeLaneChange(1)

                else:
                    changed = self.safeLaneChange(-1)

        return changed

    # Log message including car colour (could swap for id or equivalent)
    def log(self, *message):
        print(self.number, *message)
