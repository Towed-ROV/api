import queue
from typing import List

DEFAULT_PAYLOAD = {"payload_name": "", "payload_data": []}
RESPONSE = "response"
SENSOR_DATA = "sensor_data"


class Payload:
    """This class is tailored to represent a payload,
    if subsequenct calls to self is called without succes,
    the previous payload is used
    """

    def __init__(self, payload_id, queue):
        self.payload = DEFAULT_PAYLOAD
        self.payload_id = payload_id
        self.queue = queue
        self.MAX_COPIES = 1
        self.copies = 0

    def get(self):
        try:
            self.payload = self.queue.get(block=False)
        except queue.Empty:
            # Only count valid payloads
            self.verify_on("response", self.payload)
        finally:
            self.validate_on("response")
        return self.payload

    @staticmethod
    def has_data(payload):
        if payload["payload_data"]:
            return True
        return False

    @staticmethod
    def is_response(payload):
        return payload["payload_name"] == "response"

    @staticmethod
    def is_sensor_data(payload):
        return payload["payload_name"] == "sensor_data"

    def reset(self):
        self.payload = DEFAULT_PAYLOAD
        self.copies = 0

    def verify_on(self, name, payload):
        """checks if previous payloads has been used, it limit exceeded the payload is reset """
        if Payload.has_data(payload):
            if name == "response":              # Check name
                if Payload.is_response(payload):  # Check payload
                    self.copies += 1

    def validate_on(self, name):
        """resets whenever we've re-used the current stored payload too many times
        if this isnt used, the payload will continously be sent the control-app, even if the sensordata has stopped.
        """
        if name == RESPONSE:
            if self.copies > self.MAX_COPIES:
                self.reset()
                print("RESET RESPONSE")
        elif name == SENSOR_DATA:
            pass


class PayloadReceiver:
    """ This class is tailored to act as a collector for
    consuming the data from the various child-payload providers
    (ZMQ-subscribers). Will continously poll the payloads for data,
    sort them in order and finally will yield it as server-sent event to the control-application. 
    """

    def __init__(self):
        self.payloads: Payload = []
        self.known_responses = []

    def add_queue(self, input_queue):
        # TODO: Check instance types?
        _id = len(self.payloads) + 1
        payload = Payload(_id, input_queue)
        self.payloads.append(payload)

    def add_queues(self, input_queues: List):
        for queue in input_queues:
            self.add_queue(queue)

    def get_payloads(self):
        return [payload.get() for payload in self.payloads]

    def get_all(self):
        payloads = self.get_payloads()
        response_payload = PayloadReceiver.filter_and_merge(
            payloads, "response")
        sensor_data_payload = PayloadReceiver.filter_and_merge(
            payloads, "sensor_data")

        # We priorities responses
        if response_payload["payload_data"]:
            # Max 2 copies of identical responses will be allowed, check Payload-class for details
            return response_payload
        elif sensor_data_payload["payload_data"]:
            return sensor_data_payload
        else:
            return None

    @staticmethod
    def filter_and_merge(payloads, filter_name):
        filterd_payloads = PayloadReceiver._filter_names(payloads, filter_name)
        merged_and_filtered__payloads = PayloadReceiver._merge_data(
            filterd_payloads, filter_name)
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
    pass
