from random import randint
import main as sim
import json
import globalVariables as gV
from importlib import reload
import time
from os import makedirs, path

simulations = {
    "laneCount": [2, 3, 4],
    "arrivalRate": [0.75, 1, 1.25, 1.5, 1.75],
    "maxSpeedDist": [
        {
            "name": "70-60",
            "data": {
                "car": (70/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
                "van": (70/2.237, 5/2.237),
                "HGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        },
        {
            "name": "60-60",
            "data": {
                "car": (60/2.237, 5/2.237), # mean of 60 mph, std of 5 mph
                "van": (60/2.237, 5/2.237),
                "HGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        },
        {
            "name": "50-50",
            "data": {
                "car": (50/2.237, 5/2.237), # mean of 50 mph, std of 5 mph
                "van": (50/2.237, 5/2.237),
                "HGV": (50/2.237, 5/2.237)  # mean of 50 mph, std of 5 mph
            }
        },
        {
            "name": "40-40",
            "data": {
                "car": (40/2.237, 5/2.237), # mean of 40 mph, std of 5 mph
                "van": (40/2.237, 5/2.237),
                "HGV": (40/2.237, 5/2.237)  # mean of 40 mph, std of 5 mph
            }
        }
    ],
    "vehicleWeighting": [
        {
            "name": "100-0",
            "data": {
                "car": 1.00, 
                "van": 0,
                "HGV": 0  
            }
        },
        {
            "name": "75-25",
            "data": {
                "car": 0.75,
                "van": 0,
                "HGV": 0.25 
            }
        },
        {
            "name": "50-50",
            "data": {
                "car": 0.50,
                "van": 0,
                "HGV": 0.50 
            }
        },
        {
            "name": "25-75",
            "data": {
                "car": 0.25,
                "van": 0,
                "HGV": 0.75 
            }
        },
        {
            "name": "0-100",
            "data": {
                "car": 0,
                "van": 0,
                "HGV": 1
            }
        },
    ]
}

obstacles = {
    "control": [
    ],
    "2000mlane0": [
        {
            "lane": 0,
            "x": 2000
        }
    ]
}

start = time.time()
for key, obstacleObj in obstacles.items():
    if not path.exists("/".join(["data", key])):
        makedirs("/".join(["data", key]))
    for variable, values in simulations.items():
        print("Starting simulations for", variable)
        data = {}
        reload(gV)
        gV.obstacles = obstacleObj
        for val in values:
            if isinstance(val, dict):
                name = val['name']
                val = val['data']
            else:
                name = val
            print(key, variable, val, "started")

            gV.__dict__[variable] = val
            data[name] = sim.runSim(display=False, maxSimTime=60*60, seed=randint(0, 100000))

        with open("/".join(["data", key, variable + ".json"]), "w") as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

print("Done in", str(time.time() - start), "seconds")

sim.stop()
