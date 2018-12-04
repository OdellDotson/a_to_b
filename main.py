from policy import *
from simulator import *
from world import *
from request_list_helper import randomlyGenerateRequest
import json
import sys

## Initialize simulation settings, generate policy and simulator objects as well as world state object
request_list_data = { 'requests': [{'name': 'Elon','start': (3,5),'end': (8,7)},{'name': 'George','start': (2,1),'end': (3,4)}]}
simulationLenth = 1000 # time steps we take total before ending simulation
simulationCounter = 0
request_frequency = 5 # How often a new request will be added to the list.
request_list = json.dumps(request_list_data) # Dump JSON to string
request_list = json.loads(request_list) # Load json string into python dict. This also transforms the start/end tuples into a python list, ie 'start': (3,5) -> 'start': [3,5]
policy = nearestPointPolicy() # select a policy
sim = Simulator() # select a simulator
world = worldState(10, 10, 0, 0) # create default 10x10 world with car at (0,0)


## Apply any user settings. If settings not found or not of the right type, the exception handlers catch this
print("Your simulation arguments are: " , sys.argv[1::])
if len(sys.argv) <3:
    print('You did not supply enough arguments to customize the simulation. '
          'Running with default settings')
try:
    world.xStreetCount = int(sys.argv[1])
    world.yStreetCount = int(sys.argv[2])
except ValueError:
    print("You have to give integer dimensions as arg 1 and 2, I got something I couldn't turn into a map! "
          "Running with default settings of 10x10")
except IndexError:
    print("Not enough world dimensions supplied. "
          "Running with default world size of 10x10.")

try:
    simulationLenth = int(sys.argv[3])
except ValueError:
    print("The third argument must be an integer, which is how many time steps the simulation will go through! "
          "Running with default simulation length of 1000")
except IndexError:
    print("No simulation length given. "
          "Running with default simulation length of 1000")



print('---- Simulation Time = 0 ----')
print('Car initial location: ', world.car_location)
print(request_list)
## Start Simulation!
while simulationCounter < simulationLenth:
    print('---- Simulation Time =', simulationCounter +1, '----')

    # keep track of world state object and updated request list
    world, request_list = sim.stepTime(policy, world, request_list)

    # Print the updated request list after that time step
    print("Current requests: ",request_list)

    # Print the important info about out world state
    world.printWorldData()

    # This generates a new random request for the car every {request_frequency} time steps.
    if simulationCounter % request_frequency == 0: # every request_frequency time steps, generate a new random request
        request_list = randomlyGenerateRequest(request_list, world.xStreetCount, world.yStreetCount)

    simulationCounter = simulationCounter + 1

