import pickle
import json
import copy
import time

if __name__ == "__main__":

    stuff = {
        'payload_name': 'sensor_data',
        'payload_data': [
            {'name': 'roll', 'value': 147},
            {'name': 'pitch', 'value': 147},
            {'name': 'yaw', 'value': 147},
            {'name': 'pressure', 'value': 147},
            {'name': 'oxygen', 'value': 147},
            {'name': 'depth', 'value': 147},
            {'name': '2_roll', 'value': 174},
            {'name': '2_pitch', 'value': 174},
            {'name': '2_yaw', 'value': 174},
            {'name': '2_pressure', 'value': 174},
            {'name': '2_oxygen', 'value': 174},
            {'name': '2_depth', 'value': 174}
        ]
    }

    start = time.time()
    cnts = 0
    while cnts < 100000:
        item_1 = copy.deepcopy(stuff)
        cnts += 1
    # item_1["payload_data"].insert(0, {"yo": 123})
    print("Deepcopy: -- ", str(time.time() - start))

    start = time.time()
    laps = 0
    while laps < 100000:
        item_2 = pickle.loads(pickle.dumps(stuff))
        laps += 1
    # item_2["payload_data"].insert(0, {"yo": 123})
    print("Pickle  : -- ", str(time.time() - start))

    start = time.time()
    laps = 0
    while laps < 100000:
        item_2 = json.loads(json.dumps(stuff))
        laps += 1
    # item_2["payload_data"].insert(0, {"yo": 123})
    print("JSON    : -- ", str(time.time() - start))


