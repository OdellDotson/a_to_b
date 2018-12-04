import request_list_helper
import math

class worldState:
    def __init__(self, worldX, worldY, carX, carY):
        self.xStreetCount = worldX
        self.yStreetCount = worldY
        self.car_location = (carX,carY)
        self.car_passengers = []

    def distTwoPoints(self, a, b):
        """
        takes two xy-tuples and returns the distance between them
        :param a: (x1,y1)
        :param b: (x2,y2)
        :return: distance from a to b
        """
        x1, y1 = a
        x2, y2 = b
        return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2)) # distance formula

    def getNearestPoint(self, request_list, verb):
        """
        This method gets the nearest point that matches a given verb.
        Acceptable verbs are 'start' and 'end', corrosponding to the pickup and dropoff actions.
        This lets us search points of interest by verb.
        :param request_list:
        :param verb:
        :return:
        """
        if not self.car_passengers and verb == 'end': # if the passenger list is empty and dropoff mode, no one to drop off!
            return None, None

        if not request_list: # if no requests are being made, and there are no passengers, also nothing to do.
            return None, None

        nearestPoint = request_list[0][verb] # take first point to be nearest, below this will be updated
        minDistance = self.distTwoPoints(self.car_location, nearestPoint)

        # Determine which point of interest is actually the nearest to the car.
        for passenger in request_list:
            distanceToPassenger = self.distTwoPoints(self.car_location, passenger[verb])

            if distanceToPassenger < minDistance:
                nearestPoint = passenger[verb]
                minDistance = distanceToPassenger

        return nearestPoint, minDistance

    def getNearestDropoff(self):
        return self.getNearestPoint(self.car_passengers, 'end')[0]

    def getNearestDropoffAndDistanceTo(self):
        return self.getNearestPoint(self.car_passengers, 'end')

    def getNearestPickup(self, request_list):
        return self.getNearestPoint(request_list['requests'], 'start')[0]

    def getNearestPickupAndDistanceTo(self, request_list):
        return self.getNearestPoint(request_list['requests'], 'start')

    def printWorldData(self):
        print("Car location: ", self.car_location)
        print("List of all passengers:")
        for passenger in self.car_passengers:
            print("   " + passenger['name'] + ", who is headed to", passenger['end'])