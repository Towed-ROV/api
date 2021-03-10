from numpy.random import randint 
import random
from threading import Event
import queue

def get_val():
    return random.randint(1, 100)

headers = ["temperature", "kelvin", "oxygen", "pressure", "depth"]
payload = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload1 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload2 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload3 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload4 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload5 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payload6 = {
    "payload_name": "settings_data",
    "payload_data": [
        {
            "name": "temperature",
            "value": get_val(),
        },
        {
            "name": "kelvin",
            "value": get_val(),
        },
        {
            "name": "oxygen",
            "value": get_val(),
        },
        { 
            "name": "pressure",
            "value": get_val(),
        },
        {
            "name": "depth",
            "value": get_val(),
        },
    ]
}

payloads = []
payloads.append(payload)
payloads.append(payload1)
payloads.append(payload2)
payloads.append(payload3)
payloads.append(payload4)
payloads.append(payload5)
payloads.append(payload6)



from data_saver import DataSaver
import time

data_queue = queue.Queue()
exit_flag = Event()

data_saver = DataSaver(data_queue=data_queue, exit_flag=exit_flag)
data_saver.start()

for pay in payloads:
    data_queue.put(pay)
    time.sleep(0.05)

exit_flag.set()


 