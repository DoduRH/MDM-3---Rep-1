# A lovely home for all our global variables

# pygame variables
displaySize = (1400, 600)
fps = 144
deltaTime = 0
runTimer = 0

# colour bank
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (211, 211, 211)

# simulation variables
roadWidth = 20
# Mean cars arriving every 1 seconds (page 8 https://rosap.ntl.bts.gov/view/dot/16299/dot_16299_DS1.html)
# arrivalRate = [0.001, 0.06166666666666667, 0.06166666666666667]
arrivalRate = [0.02, 0.02, 0.02]
# arrivalRate = [0.2, 0.2, 0.2]

laneCount = 3

acceleration = 4 # need a good source of 'normal' acceleration on motorway
deceleration = -10 # https://copradar.com/chapts/references/acceleration.html#:~:text=Many%20safety%20experts%20use%2015,maximum%20braking%20around%200.8%20g's.

# Scale 1 metre = 4.44444 Pixels, 20 pixels = 4.5 metres (Need to scale this down in the future)
maxSpeedDist = (137.77764, 9.934212288) # mean of 70 mph, std of 5 mph
vehicleSizes = [20, 25, 80] # size of car, van, LGV
vehicleStartingVelocity = 137.77764/4

# Collected Data
vehicleCrossingTimes = []
