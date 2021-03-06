# Contains the road class
import pygame as pg
import globalVariables as gV
import vehicle
import obstacle
import numpy as np


class Road:

    def __init__(self, pos, laneCount, laneWidth, meanArrivalRate):
        self.pos = pos
        self.laneCount = laneCount
        self.laneWidth = laneWidth
        self.laneFlowRates = np.zeros(laneCount)
        self.meanArrivalRate = [meanArrivalRate for _ in range(laneCount)]

        self.vehicleArray = []
        self.obstructionArray = []
        self.currentCarIndex = -1
        self.font = pg.font.SysFont('Comic Sans MS', round(laneWidth - laneWidth * 0.25))

        self.spawnedVehicles = {
            "car": 0,
            "van": 0,
            "HGV": 0
        }

    def draw(self, display):
        '''
            Draw road object and cars/obstacles on it
        '''
        # Draw road
        for i in range(self.laneCount):
            pg.draw.rect(display, gV.grey,
                         [self.pos[0], self.pos[1] + self.laneWidth * i * 1.05, gV.displaySize[0], self.laneWidth])
        
        # Draw cars
        for vehicleObject in self.vehicleArray:
            vehicleObject.draw(display)

        # obstacle handling loop
        for obstacleObject in self.obstructionArray:
            obstacleObject.draw(display)

    def spawnVehicle(self, vehicleType=None, lane=None, x=None, speedLimit=None, acceleration=None, deceleration=None,
                     checkSpawn=True):
        '''
            Spawns a vehicle, uses global variables if parameters are None
        '''
        if vehicleType is None:
            vehicleOptions = list(gV.vehicleSizes.keys())
            weights = []
            for v in vehicleOptions:
                weights.append(gV.vehicleWeighting[v])

            vehicleType = np.random.choice(vehicleOptions, p=weights)
            self.spawnedVehicles[vehicleType] += 1
        vehicleSize = gV.vehicleSizes[vehicleType]

        # ensure an HGV is not being spawned in the most outer lane
        if lane is self.laneCount - 1:
            if vehicleType == 'HGV':
                # print("HGVs cannot spawn in the 3rd lane")
                lane = np.random.randint(0, self.laneCount - 1)

        if lane is None:
            if vehicleType == 'HGV' and self.laneCount >= 3:
                lane = np.random.randint(0, self.laneCount - 1)
            else:
                lane = np.random.randint(0, self.laneCount)

        if x is None:
            x = -vehicleSize

        if speedLimit is None:
            speedLimit = np.random.normal(*gV.maxSpeedDist[vehicleType])

        if acceleration is None:
            acceleration = gV.acceleration

        if deceleration is None:
            deceleration = gV.deceleration

        if checkSpawn:
            if self.carSpawnCheck(lane):
                return

        self.vehicleArray.append(
            vehicle.Vehicle(road=self, vehicleLength=vehicleSize, lane=lane, x=x,
                            speedLimit=speedLimit,
                            acceleration=acceleration,
                            deceleration=deceleration))

    def generateTraffic(self):
        for i in range(self.laneCount):
            for _ in range(0, np.random.poisson(self.meanArrivalRate[i])):
                self.spawnVehicle(lane=i)

    # Returns list of cars in specified lane
    def carsInLane(self, lane):
        return [x for x in self.vehicleArray if x.lane == lane]

    def obstaclesInLane(self, lane):
        return [x for x in self.obstructionArray if x.lane == lane]

    # returns the average velocity of vehicles in a lane
    def calcLaneFlowRate(self, lane):
        vehiclesInLane = self.carsInLane(lane)
        totalVelocity = 0
        for vehicleObject in vehiclesInLane:
            totalVelocity += vehicleObject.velocity

        if len(vehiclesInLane) != 0:
            avgVelocity = totalVelocity / len(vehiclesInLane)

        else:
            avgVelocity = 0

        self.laneFlowRates[lane] = avgVelocity

    def newCarIndex(self):
        self.currentCarIndex += 1
        return self.currentCarIndex

    # checks if a car already exists in the lane where a vehicle spawn has been requested to spawn
    # returns true if there is a car and false if it is safe to spawn car
    def carSpawnCheck(self, lane):
        for vehicles in self.vehicleArray:
            if vehicles.lane == lane and vehicles.x < 80: # must spawn 2 chevrons apart
                # print("Spawn failed")
                return True

        return False
