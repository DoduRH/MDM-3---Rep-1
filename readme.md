# Detecting and Protecting a Stationary Vehicle in a Connected World

Modelling how connected vehicles avoid a collosion on a stretch of motorway while varying lanes, speed limits, busyness and obstacles.

# How to use?

The simulations were run on Python 3.8.5 in a conda environment

## Package Requirements

* Scipy 1.5.2
* Numpy 1.19.1
* Pygame 2.0.0

## Running a simulation

To run a simple simulation and view the output run `main.py`.

`collectData.py` runs the simulation multiple times without any visualisation in order to collect data quickly and easily. It then saves the combined data to a JSON file.  `Simulations` contains the parameters that will be changed as well as the values they will be changed to.  `Obstacles` contains the name of the test as well as the position of the obstacle(s).

`globalVariables.py` controls the default values for each of the variables.