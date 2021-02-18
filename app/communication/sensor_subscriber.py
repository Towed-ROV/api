import zmq
from threading import Thread
from queue import Queue
from fastapi.encoders import jsonable_encoder


class SensorSubscriber(Thread):
    def __init__(self, sensor_queue, host: str, port: int, topic: str = ""):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.SUB)
        self.sensor_queue = sensor_queue
        self.connection.subscribe(topic)
        self.host = host
        self.port = port

    def connect(self):
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] SensorSubscriber")

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.connect()
        while True:
            data = self.recv()
            self.sensor_queue.put(data)


if __name__ == "__main__":
    pass
