from communication.video_client import VideoClient


class VideoConnection:
    """This class is tailored to act as a connection between the API and the
    separate OpenCV video-server running on the Towed-ROV
    """

    def __init__(self, host, port, img_queue, exit_flag):
        self.host = host
        self.port = port
        self.exit_flag = exit_flag
        self.img_queue = img_queue
        self.is_running = False

    def start(self):
        self.exit_flag.clear()
        vc = VideoClient(self.img_queue, self.exit_flag, self.host, self.port)
        vc.daemon = True
        vc.start()
        self.is_running = True

    def stop(self):
        self.exit_flag.set()
        self.is_running = False


if __name__ == "__main__":

    import cv2
    import queue
    from video_client import VideoClient

    video_connection = VideoConnection("XXXXXXXX", 0000)
    img_queue = video_connection.img_queue

    inp = input("Enter: ")

    video_connection.start()

    while True:
        try:
            img = img_queue.get()
            cv2.imshow("VIDEO", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except queue.Empty:
            break
        except KeyboardInterrupt:
            break

    video_connection.stop()

    inp = input("Finito?")
