from random import randint
import main as sim
import json
import globalVariables as gV
from importlib import reload
import time

simulations = {
    "laneCount": [2, 3, 4],
    "arrivalRate": [0.1, 0.2, 0.3],
    "maxSpeedDist": [
        {
            "car": (70/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
            "van": (70/2.237, 5/2.237),
            "LGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
        },
        {
            "car": (60/2.237, 5/2.237), # mean of 60 mph, std of 5 mph
            "van": (60/2.237, 5/2.237),
            "LGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
        },
        {
            "car": (50/2.237, 5/2.237), # mean of 50 mph, std of 5 mph
            "van": (50/2.237, 5/2.237),
            "LGV": (50/2.237, 5/2.237)  # mean of 50 mph, std of 5 mph
        },
        {
            "car": (40/2.237, 5/2.237), # mean of 50 mph, std of 5 mph
            "van": (40/2.237, 5/2.237),
            "LGV": (40/2.237, 5/2.237)  # mean of 50 mph, std of 5 mph
        }
    ],
    "acceleration": [2, 3, 4, 5, 6],
    "deceleration": [-6, -8, -10, -12, -14]
}

start = time.time()

for variable, values in simulations.items():
    print("Starting simulations for", variable)
    data = {}
    reload(gV)
    for val in values:
        print(val, "started")
        gV.__dict__[variable] = val
        data[str(val)] = sim.runSim(display=False, maxSimTime=60*60, seed=randint(0, 100000))


    with open("data/" + variable + ".json", "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

print("Done in", str(time.time() - start), "seconds")

sim.stop()