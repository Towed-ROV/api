from multiprocessing import Queue
from typing import List
import queue
import time

DEFAULT_PAYLOAD = {"payload_name": "default", "payload_data": []}

class Payload:
    def __init__(self, payload_id, queue):
        self.payload = DEFAULT_PAYLOAD
        self.payload_id = payload_id
        self.queue = queue

    def get(self):
        try:
           self.payload = self.queue.get(block=False)
        except queue.Empty:
            pass 
        return self.payload

class PayloadReceiver:
    def __init__(self):
        self.payloads: Payload = []

    def add_queue(self, input_queue):
        # TODO: Check instance types?
        temp_id = len(self.payloads)
        payload = Payload(temp_id, input_queue)
        self.payloads.append(payload)

    def add_queues(self, queues: List):
        for queue in queues:
            self.add_queue(queue)

    def get_payloads(self):
        return [payload.get() for payload in self.payloads]
    
    def get_all(self):
        payloads = self.get_payloads()
        response_payload = PayloadReceiver.filter_and_merge(payloads, "response")
        sensor_data_payload = PayloadReceiver.filter_and_merge(payloads, "sensor_data")

        # We priorities responses
        if response_payload["payload_data"]:
            return response_payload
        elif sensor_data_payload["payload_data"]:
            return sensor_data_payload
        else:
            return None

    @staticmethod
    def filter_and_merge(payloads, filter_name):
        filterd_payloads = PayloadReceiver._filter_names(payloads, filter_name)
        merged_and_filtered__payloads = PayloadReceiver._merge_data(filterd_payloads, filter_name)
        return merged_and_filtered__payloads

    @staticmethod
    def _filter_names(payloads, filter_name):
        return [payload for payload in payloads if payload["payload_name"] == filter_name]

    @staticmethod
    def _merge_data(payloads, payload_name: str):
        merged_payload = {"payload_name": payload_name, "payload_data": []}
        sensor_names = []
        for payload in payloads:
            for sensor in payload["payload_data"]:
                sensor_name = sensor["name"]
                if sensor_name not in sensor_names:
                    merged_payload["payload_data"].append(sensor)
                    sensor_names.append(sensor_name)
        return merged_payload

if __name__ == "__main__":

    sensor_q_1 = Queue()
    sensor_q_2 = Queue()
    
    payload_recvr = PayloadReceiver()
    payload_recvr.add_queue(sensor_q_1)
    payload_recvr.add_queue(sensor_q_2)

    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
    print("")
    sensor_q_1.put({"payload_name": "sensor_data", "payload_data": [{"name": "heat", "value": 1}]})
    sensor_q_2.put({"payload_name": "response", "payload_data": [{"name": "heat1", "success": True}]})
    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
    payloads = payload_recvr.get_all()
    print(payloads) # EMPTY
