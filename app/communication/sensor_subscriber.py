from multiprocessing import Process
from threading import Thread
from queue import Queue
import zmq
import time


class SensorSubscriber(Process):
    """Basic ZMQ subscriber running in a seperate process to poll data from the Towed-ROV
    
    SUB / PUB is connectionless, so it doesnt care if you disconnect, it will 
    continously try to re-read from the socket. So any disconnect / reloads or similar doesnt matter,
    because the subscriber will always listen for reconnects
    """
    def __init__(self, data_queue, host: str, port: int):
        Process.__init__(self)
        self.data_queue = data_queue
        self.connection = None
        self.ctx = None
        self.host = host
        self.port = port

    def init(self):
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.SUB)
        self.connection.subscribe("")
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] SensorSubscriber")

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.init()
        while True:
            data = self.recv()
            self.data_queue.put(data)

if __name__ == "__main__":

    ctx = zmq.Context()
    connection = ctx.socket(zmq.SUB)
    connection.subscribe("")
    connection.connect("tcp://127.0.0.1:8787")

    for x in range(10):
        print(connection.recv_string())