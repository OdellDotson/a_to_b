import math

class AbstractPolicy:
    """
    AbstractPolicy: abstract class that defines the interface between a policy to the simulation
    """
    def __init__(self):
        raise NotImplementedError

    def getNextStep(self, world_state, request_list):
        """
        This method is the main exposed part of a policy. It should take in a world state and a request list
        and return the policy's decided action
        """
        raise NotImplementedError

class nearestPointPolicy(AbstractPolicy):
    """
    This policy determines which is the nearest point and drives to it.
    Drop-offs are prioritized if there is a dropoff and a pickup the same distance from the car.
    """
    def __init__(self):
        pass

    def getDirectionsToPoint(self, world_state, point):
        """
        Gets directions to the point given.
        Very simple pathing function, will simply go in the x direction if x and y dimensions have the same error,
        unless that same error is zero.

        This is our basic "path planner", it simply determines a direction to go based on the vector of the
        error between the desired current point and the current car location.

        :param world_state: world state object to get car location info from
        :param point: (x, y)    tuple that represents target of car
        :return: (x, y)   returns a tuple of x, y motion that represents how the car should next move to get to point
        """

        x1, y1 = point
        x2, y2 = world_state.car_location

        if x1 == x2 and y1 == y2: # if we're being told to path to where we are...
            return 0, 0

        if abs(x1-x2) > abs(y1-y2): # if there is greater error in the x dimension, go along an x street
            if x2 > x1:
                return -1, 0, # go east
            else:
                return 1, 0 # go west
        else: # otherwise, correct error in the y direction
            if y2 > y1:
                return 0, -1, # go south
            else:
                return 0, 1 # go north

    def getNextStep(self, world, request_list):
        """
        Determines nearest pickup and nearest dropoff locations
        Goes to closest of the two.
        If dropoff and pickup are both same distance, prioritize dropoff.
        """
        nearest_dropoff, nearest_dropoff_dist = world.getNearestDropoffAndDistanceTo()
        nearest_pickup, nearest_pickup_dist = world.getNearestPickupAndDistanceTo(request_list)

        if nearest_dropoff is None and nearest_pickup is None:
            return 0,0 # TODO pathing back to the center would be better than just sitting there...
        if nearest_dropoff is None: # If there is no pick up, just go to nearest dropoff
            return self.getDirectionsToPoint(world, nearest_pickup)
        if nearest_pickup is None: # If there is no dropoff, just go to nearest pickup
            return self.getDirectionsToPoint(world, nearest_dropoff)

        if nearest_pickup_dist == nearest_dropoff_dist:
            return self.getDirectionsToPoint(world, nearest_dropoff) # if pickup and dropoff are equal distance away, drop off
        else: # otherwise, go to nearest point.
            if nearest_dropoff_dist < nearest_pickup_dist:
                return self.getDirectionsToPoint(world, nearest_dropoff)
            else:
                return self.getDirectionsToPoint(world, nearest_pickup)

class pointCentroidPolicy(AbstractPolicy):
    """
    This policy is based on two ideas:
        1. We should always be driving towards the area with the greatest density of pickups/dropoffs
        2. We should attempt to drop off or pick up passengers who are "on the way" to the centroid of pickups and dropoffs
    I didn't get to implementing this within 5 hours of working on this project, so it remains unimplemented.

    The following is some psudocode for how I'd like to take the two a ideas into account in a policy.


        centroid = getAveragePointOfInterest() # average the x, y of all pickups and dropoffs.

        lineToCentroid = getLineSegBetweenToPoints(car_location, centroid) # Get the line segment that describes the distance from car to center of pickup/dropoff activity

        # getPointNearestToLine() is a function that should return the pickup/dropoff that is nearest to the line given
        # The idea here is that we define a line between the car and the area where "most" cars are, and then
        # path to whichever car is nearest to that line. This would allow the car to pick people up along the way to the area of
        # greatest request density, or even drive away from the centroid if the nearest request is closer to the line than any other point.
        target_location = getPointNearestToLine(lineToCentroid)

    """

    def __init__(self):
        pass

    def getNextStep(self, world_state, request_list):
        raise NotImplementedError
