from threading import Thread

import zmq


class CommandDispatcher(Thread):
    """This class is tailored to represent a ZMQ Requester
    for sending commands down to the Towed-ROV

    Args:
        Thread (inherits): subclassed in a limited fashion
    """

    def __init__(self, cmd_queue, host="127.0.0.1", port=1337):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REQ)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def connect(self):
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] CommandDispatcher")

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.connect()
        while True:
            try:
                cmd = self.cmd_queue.get()
                self.send(cmd)             # Send to ROV
                self.cmd_queue.task_done()
                _ = self.recv()            # Recv from ROV
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":

    """ TESTING """

    import queue
    import time

    cmd_send_queue = queue.Queue()
    cd = CommandDispatcher(cmd_send_queue)
    cd.start()

    cmd_payload = {"cmd": None}

    while True:
        try:
            input_command = input("> ")
            cmd_payload["cmd"] = input_command
            cmd_send_queue.put(cmd_payload)
        except KeyboardInterrupt:
            break
