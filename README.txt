################################### Autonomous Vehicle Simulator

This software simulates a car controlled by a simple policy to pick up and drop off riders.

New ride requests are randomly generated every 5 turns (this variable can be changed easy)

The world size and simulation length are controlled by command line inputs.

Some other aspects of the simulation can be controlled via variables in main.py

################################### Requirements

This project was developed using a Python 3.6.1 interpreter. I have not tested compatibility with other versions of Python.
Probably will run on any version of python3, but if you have trouble make sure you're using 3.6.1

All libraries used are part of the python standard library, so there are no dependencies outside of a Python 3.6.1 interpreter.

################################### Running the simulation
## Note: If long simulations are run (more than 10 steps) you may want to pipe the output to a file:
##		python3 main.py > output.log
## I added more logging than was requested in the problem statment because I believe it was useful
## and provides a telling trace of the sim. However, once I started running simulations longer than 5000
## time steps, I just started pipeing all output to a file so I could easy review it.
## A quick warning: Log files can grow quite large if using a longrunning simulation, as I print the request list on every time step!
## A 10x10 map with a simulation length of 1,000,000 produced a 600+MB log!
## A good future feature would be to have a default logging file for all simulations.

## Note: I'm developing on a macbook, and to run my python3 interpreter, I use the `python3` command.
## If you have a python3.6.1+ interpreter bound to `python`, then don't worry about using `python3`, just use your stadard `python`

from the root directory of the project, run main.py with the following format of arguments:

	python3 main.py [world's x dimension] [world's y dimension] [simulation length]

for example:

	python3 main.py 16 14 500

would generate a 16x14 world and run the simulation for 500 steps.

If not enough arguments are supplied, the simulation will rely on defaults. For example:

	python3 main.py 13 19

This is sufficient to run the simulation. It will run 1000 steps on a 13x19 world, the default simulation length with a custom world size.

	python3 main.py

This is also sufficient to run the simulation. It will run 1000 steps on a 10x10 world, using all default settings.

################################### Simulation Configuration

All defaults are stored in variables at the top of main.
Defaut world size is 10 by 10
Default simulation length is 1000 time steps
Defaul request_frequency is 5. This determines the frequency of new requests. Every n turns, a new request is generated.
There is also an initial hard-coded request list stored in the main.py

Eventually these configs should be moved to a JSON file and read in by the program, but for this size of project I thought that wasn't necessary.

################################### Software overview

Here's a quick rundown on the files and their purpose:

	README.txt
		You are here!

	problem.txt
		problem statement

	main.py
		main function
		rocesses user input
		instantiates required objects and runs simulation, prints statistics

	world.py
		our worldState class is defined here
			keeps track of data like the car's location and passenger list
		provides funcionality related to world state, such as printWorldData() or getNearestDropoff()

	simulator.py
		our Simulator class is defined here
			handles running a policy on a world state and updating the world state as needed

	policy.py
		defines an abstract Policy class, which requires a getNextStep() method from all policies
		has implementation of one policy, based on travelling to the nearest neighbor
		has some documentation for a planned policy that I didn't get to implementing

	request_list_helper.py
		has code for randomly generating new request dictionaries for the simulator.

Inline documentation is also present, which provides a more thorough expliation of the code.

################################### Notes

I've noticed something somewhat interesting about the algorithm's behavior on a 10x10 map when generating a new reqeust each 5 t-steps.
It seems to reach a steady state of delivering about 2 passengers every 10 time steps, with an average of <10 passengers and <10 active requests.

Running the simulation for T=100 resulted in 15 passengers delivered. (Ran a few, average seems to be 15 or so)
Running the simulation for T=1,000 resulted in 192 passengers delivered.
Running the simulation for T=10,000 resulted in 1992 passengers delivered.
Running the simulation for T=100,000 resulted in 19989 passengers delivered.
Running the simulation for T=1,000,000 resulted in 199992 passengers delivered.

At the end of the T=100,000 simulation, the car has only 8 passengers and 5 requests, which I was surprised by.
At the end of the T=1,000,000 simulation, the car had only 3 passengers and 7 requests, so it does seem to be a steady state.

This made me wonder about settling time of different policies, map sizes, and request rates.

##

