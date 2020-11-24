from random import randint
import main as sim
import json
import globalVariables as gV
from importlib import reload
import time
from os import makedirs, path

simulations = {
    "laneCount": [2, 3, 4],
    "arrivalRate": [0.1, 0.2, 0.3],
    "maxSpeedDist": [
        {
            "name": "70-60",
            "data": {
                "car": (70/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
                "van": (70/2.237, 5/2.237),
                "LGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        },
        {
            "name": "60-60",
            "data": {
                "car": (60/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
                "van": (60/2.237, 5/2.237),
                "LGV": (60/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        },
        {
            "name": "50-50",
            "data": {
                "car": (50/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
                "van": (50/2.237, 5/2.237),
                "LGV": (50/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        },
        {
            "name": "40-40",
            "data": {
                "car": (40/2.237, 5/2.237), # mean of 70 mph, std of 5 mph
                "van": (40/2.237, 5/2.237),
                "LGV": (40/2.237, 5/2.237)  # mean of 60 mph, std of 5 mph
            }
        }
    ],
    "acceleration": [2, 3, 4, 5, 6],
    "deceleration": [-6, -8, -10, -12, -14]
}

simulations = {
    "arrivalRate": [0.1, 0.2, 0.3],
}

start = time.time()

for variable, values in simulations.items():
    print("Starting simulations for", variable)
    data = {}
    reload(gV)
    foldername = "CSVData/" + variable
    if not path.exists(foldername):
        makedirs(foldername)
    for val in values:
        if isinstance(val, dict):
            name = val['name']
            val = val['data']
        else:
            name = val
        print(val, "started")


        gV.__dict__[variable] = val
        data[name] = sim.runSim(display=False, maxSimTime=60*60, seed=randint(0, 100000))
        #with open("CSVData/" + variable + "/" + str(name) + ".csv", "w") as outfile:
        #    outfile.writelines("\n".join([str(x) for x in data[name]['averageVelocityTotal']]))


    with open("data/" + variable + ".json", "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

print("Done in", str(time.time() - start), "seconds")

sim.stop()