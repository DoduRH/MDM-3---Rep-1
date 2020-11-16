# A lovely home for all our global variables

# pygame variables
displaySize = (1000, 600)
fps = 60
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
roadWidth = 40
roadSpeedLimit = 100
# Mean cars arriving every 1 seconds (page 8 https://rosap.ntl.bts.gov/view/dot/16299/dot_16299_DS1.html)
# arrivalRate = [0.001, 0.06166666666666667, 0.06166666666666667]
arrivalRate = [0.02, 0.02, 0.02]

laneCount = 3

acceleration = 3 # need a good source of 'normal' acceleration on motorway
deceleration = -10 # https://copradar.com/chapts/references/acceleration.html#:~:text=Many%20safety%20experts%20use%2015,maximum%20braking%20around%200.8%20g's.

maxSpeedDist = (30, 2.2) # mean of 70 mph, std of 5 mph

# Collected Data
vehicleCrossingTimes = []
