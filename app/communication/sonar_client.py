# from multiprocessing import Process, Event, Queue
import struct
import pickle
import cv2
import numpy as np
import zmq
import socket
import queue
from multiprocessing import Process, Queue
import time

class SonarPlotter:
    def __init__(self, dimention: tuple = (500, 1000)):
        self.dimention = dimention
        self.image = np.zeros(self.dimention, dtype=np.uint8)

    def pop_push_and_get(self, line: np.ndarray):
        self.pop()
        self.push(line)
        return self.image

    def push(self, input_row: np.ndarray):
        self.image = np.insert(arr=self.image, obj=0, values=input_row, axis=0)

    def pop(self):
        self.image = np.delete(arr=self.image, obj=-1, axis=0)


class SonarSubscriber(Process):
    def __init__(self, data_queue, host: str, port: int):
        Process.__init__(self)
        self.ctx = None
        self.host = host
        self.port = port
        self.connection = None
        self.data_queue = data_queue
        self.SONAR_IMG_WIDTH = 1000
        self.SONAR_IMG_HEIGHT = 500
        self.SONAR_IMG_WIDTH_HALF = 1000
        self.plotter = SonarPlotter((self.SONAR_IMG_HEIGHT, self.SONAR_IMG_WIDTH))

    def init(self):
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.SUB)
        self.connection.subscribe("")
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] SonarSubscriber")

    def recv_str(self):
        return self.connection.recv_string()

    def run(self):
        self.init()
        while True:
            msg_str = self.recv_str()       # receive raw string from C++
            row = self.msg_to_row(msg_str)  # process string into np.ndarray
            img = self.row_to_img(row)      # insert np.ndarray into top of image
            self.data_queue.put(img)        # send image to client

    def row_to_img(self, row: np.ndarray):
        return self.plotter.pop_push_and_get(row)

    def msg_to_row(self, msg_str):
        """ this method highly relies on the stringformating in the SONAR C++ code """
        msg = msg_str.strip()
        msg = msg.split(" ")
        arr = np.array([np.uint8(x) for x in msg])
        left = np.flipud(arr[:self.SONAR_IMG_WIDTH_HALF])  # reverse
        right = arr[self.SONAR_IMG_WIDTH_HALF:]
        arr[:self.SONAR_IMG_WIDTH_HALF] = left
        arr[self.SONAR_IMG_WIDTH_HALF:] = right
        return arr


if __name__ == "__main__":

    img_queue = Queue(maxsize=55)
    sonar_sub = SonarSubscriber(img_queue, host="127.0.0.1", port=5555)
    sonar_sub.start()

    print("READY FOR DATA !")
    
    while True:
        img = img_queue.get()
        img = cv2.resize(img, (640, 480)) # Good looking GUI size
        cv2.imshow("SONAR IMAGE", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

    # import threading
    
    # plt = SonarPlotter((500, 1000))
    # img_queue = queue.Queue()
    
    # def recv_and_put(input_queue):
    #     context = zmq.Context()
    #     HALF = 500
    #     receiver = context.socket(zmq.SUB)
    #     receiver.connect("tcp://127.0.0.1:5555")
    #     receiver.setsockopt_string(zmq.SUBSCRIBE, "")
    #     while True:
    #         msg = receiver.recv_string()
    #         msg = msg.strip()
    #         msg = msg.split(" ")
    #         arr = np.array([np.uint8(x) for x in msg])
    #         left = np.flipud(arr[:HALF])  # reverse
    #         right = arr[HALF:]
    #         arr[:HALF] = left
    #         arr[HALF:] = right
    #         img_queue.put(arr)

    # t = threading.Thread(target=recv_and_put, args=(img_queue,))
    # t.daemon = True
    # t.start()

    # print("READY!")
    # while True:
    #     temp_row = img_queue.get()
    #     img = plt.pop_push_and_get(temp_row)
    #     img = cv2.resize(img, (640, 480))
    #     cv2.imshow('Window', img)
    #     if cv2.waitKey(1) == ord('q'):
    #         break
    #     img_queue.task_done()