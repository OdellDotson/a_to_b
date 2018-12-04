import json
import random
import string

def randomlyGenerateRequest(rq_list, x, y):
    """
    Takes in a request list, and world dimensions, returns a new request list with an additional request within that world.
    We might want to add a random new request if there are zero requests in queue, for example.
    """
    rq_list['requests'].append({
       'name': ''.join(random.choice(string.ascii_letters) for _ in range(6)), # this random name generator was grabbed off stack overflow, not my own work
       'start': ( random.randint(0,x),random.randint(0,y) ),
       'end': ( random.randint(0,x),random.randint(0,y) )
    })

    request_list = json.dumps(rq_list)
    request_list = json.loads(request_list) # converts tuple to list for 'start'/'end' fields

    return request_list