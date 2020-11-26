# pygame variables
displaySize = (2550, 600)
fps = 10

# colour bank
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (211, 211, 211)

roadWidth = 20 # Width of each lane

arrivalRate = 1.25 # Mean cars arriving per lane per second

laneCount = 2

acceleration = 4 # Max acceleration
deceleration = -10 # Max deceleration

# ALL IN meters AND seconds
maxSpeedDist = {
    "car": (70/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
    "van": (70/2.237, 5/2.237),
    "LGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
}

# Length of vehicles in meters
vehicleSizes = {
    "car": 4.5,
    "van": 8,
    "LGV": 18
}

scale = 1 # How many pixels per meter, only affects length left to right

obstacles = [
    {
        "lane": 0,
        "x": 2000
    }
]

# Seeding numpy to give reproducible results, set to None to generate a seed
seed = None 

# Position of the flow rate markers (meters)
flowrateChecks = [1500, 2000, 2500]
