from communication.video_client import VideoClient
from multiprocessing import Event, Queue



class VideoConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.exit_flag = Event()
        self.img_queue = Queue(maxsize=30) # ~1 seconds

    def start(self):
        self.exit_flag.clear()
        vc = VideoClient(self.img_queue, self.exit_flag, self.host, self.port)
        vc.daemon = True
        vc.start()

    def stop(self):
        self.exit_flag.set()
        self.img_queue = Queue()

if __name__ == "__main__":

    from multiprocessing import Event, Queue
    import cv2
    import queue

    img_queue = Queue(maxsize=30)
    exit_flag = Event()
    video_connection = VideoConnection("192.168.1.118", 1337, exit_flag, img_queue)

    try:
        print("Welcome.")
        while True:
            inp = input("CMD: ")
            
            if inp == "start":
                video_connection.start()

            while True:
                try:
                    img = img_queue.get()
                    cv2.imshow("VIDEO", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except queue.Empty:
                    pass

    except Exception:
        video_connection.stop()