import numpy as np
import struct
import pickle
import cv2
import threading
import socket
import queue
import time

class VideoClient(threading.Thread):
    def __init__(self, image_queue, exit_flag, host="192.168.1.119", port=1337):
        threading.Thread.__init__(self)
        self.image_queue = image_queue
        self.exit_flag = exit_flag
        self.host = host
        self.port = port
        self.connection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.data = b""
        self.PAYLOAD_SIZE = struct.calcsize(">L")

    def connect(self):
        try:
            self.connection.connect((self.host, self.port))
            print("[STARTED] VideoClient")

        except TimeoutError:
            print("Connection : TimeoutError: ", self.host, ":", self.port)

    def disconnect(self):
        try:
            self.connection.close()
            self.is_running = False
        except Exception:
            print("Cant close shitt")
        finally:
            print("[STOPPED] VideoClient")

    def run(self):
        self.connect()
        time.sleep(2)
        while not self.exit_flag.is_set():
            frm = self.get_frame()
            self.image_queue.put(frm)
        self.disconnect()

    def get_frame(self):
        while len(self.data) < self.PAYLOAD_SIZE:
            self.data += self.connection.recv(4096)
        packed_msg_size = self.data[:self.PAYLOAD_SIZE]
        self.data = self.data[self.PAYLOAD_SIZE:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.connection.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(
            frame_data, fix_imports=True, encoding="bytes")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)


if __name__ == "__main__":

    img_queue = queue.Queue(maxsize=15)
    exit_flag = threading.Event()

    cv = VideoClient(img_queue, exit_flag, "192.168.0.102", 1337)
    cv.setDaemon(True)
    cv.start()

    while True:
        img = img_queue.get()
        cv2.imshow("VIDEO", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        img_queue.task_done()

    
    cv2.destroyAllWindows()
