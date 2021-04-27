from multiprocessing import Event, Queue
from sonar_subscriber import SonarSubscriber
# from communication.sonar_subscriber import SonarSubscriber
class SonarConnection:
     """Basic ZMQ subscriber running in a seperate process to poll data from the Sonar-API
    
    SUB / PUB is connectionless, so it doesnt care if you disconnect, it will 
    continously try to re-read from the socket. So any disconnect / reloads or similar doesnt matter,
    because the subscriber will always listen for reconnects
    """
    def __init__(self, host, port, img_queue, exit_flag):
        self.host = host
        self.port = port
        self.exit_flag = exit_flag
        self.img_queue = img_queue
        self.is_running = False

    def start(self):
        self.exit_flag.clear()
        vc = SonarSubscriber(self.img_queue, self.exit_flag, self.host, self.port)
        vc.start()
        self.is_running = True

    def stop(self):
        self.exit_flag.set()
        self.is_running = False
        

if __name__ == "__main__":

    import cv2
    import queue
    import threading

    img_queue = Queue()
    exit_flag = Event()

    sonar_connection = SonarConnection("127.0.0.1", 8787, img_queue, exit_flag)

    def endpoint(qq):
        while True:
            img = qq.get()
            cv2.imshow("VIDEO", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    t = threading.Thread(target=endpoint, args=(img_queue,))
    t.daemon = True
    t.start()

    sonar_connection.start()


    while True:
        cmd = input("CMD: ")

        if cmd == "status":
            print("status: ", sonar_connection.is_running)

        if cmd == "start":
            sonar_connection.start()

        if cmd == "stop":
            sonar_connection.stop()

        if cmd == "quit":
            break
        

    inp = input("Finito?")