class Simulator:
    """
    The simulator takes in a policy and a world_state, and determines the next world state based on that policy.
    """
    def __init__(self):
        self.droppedOff = 0 # Stuck this in here as a way to cheaply see stats for a simulator, even if the policy changes
        pass

    def applyPolicy(self, policyChoice, world_data, request_list):
        """
        This method applies the choice selected by the policy to the simulation model
        :param policyChoice: The selected action from the policy
        :param world_data: The simulation model
        :param request_list: The request list. (This is needed so that we can remove people we pick up.)
        :return: Updated world_data, request_list
        """
        deltaX, deltaY = policyChoice

        prevX, prevY = world_data.car_location

        # We need to check both before and after moving if there is anyone here to be picked up or dropped off.
        # This is to cover the edge case in which a new request is added to the request_list with a
        # 'start' location that equals the car's current position.
        # I am making the assumption that we can pick them up before we start driving again, as it seems that
        # pickup/dropoff actions take 0 time for this problem.
        world_data, request_list = self.pickupAndDropoff(world_data, request_list)

        world_data.car_location = (prevX + deltaX, prevY + deltaY)

        world_data, request_list = self.pickupAndDropoff(world_data, request_list)

        return world_data, request_list

    def pickupAndDropoff(self, world_data, request_list):
        """
        This method simply picks up and drops off anyone who can be, at the car's current location.
        """
        x1, y1 = world_data.car_location

        # Remove any passengers from passenger list who are going to the current location
        new_car_passengers = []
        for passenger in world_data.car_passengers:
            if passenger['end'] != [x1, y1]:
                new_car_passengers.append(passenger)
            else:
                self.droppedOff = self.droppedOff + 1 # some quick logging for my own curiosity. Simulator statistics should probsbly have a more refined protocol than this.

        # Remove any requests originiating from the current location and add them to the passenger list
        new_request_list = {'requests':[]}
        for request in request_list['requests']:
            if request['start'] == [x1, y1]:
                new_car_passengers.append(request)
            else:
                new_request_list['requests'].append(request)

        # update world model with new passenger list
        world_data.car_passengers = new_car_passengers

        return world_data, new_request_list

    def stepTime(self, policy, world_data, request_list):
        """
        Update a world model and request list according to a policy
        :param policy:
        :param world_data:
        :param request_list:
        :return:
        """
        policy_choice = policy.getNextStep(world_data, request_list) # Given world state, determine policy's choice
        print('Policy choice: Move by', policy_choice)
        new_world, new_request_list = self.applyPolicy(policy_choice, world_data, request_list) # Apply policy choice
        print('Total dropped off passengers after policy applied:', self.droppedOff)

        return new_world, new_request_list