import zmq
from threading import Thread
from multiprocessing import Process
from queue import Queue
import time

class SensorSubscriber(Process):
    def __init__(self, data_queue, host: str, port: int):
        Process.__init__(self)
        self.data_queue = data_queue
        self.connection = None
        self.host = host
        self.port = port

    def init(self):
        self.connection = zmq.Context().socket(zmq.SUB)
        self.connection.subscribe("")
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] SensorSubscriber")

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.init()
        while True:
            data = self.recv()
            self.data_queue.send(data)


if __name__ == "__main__":

    # sensor_queue = Queue()
    sensor_sub = SensorSubscriber(host="192.168.1.118", port=8001)
    sensor_sub.daemon = True
    sensor_sub.start()
    time.sleep(2)
    print("Done")
