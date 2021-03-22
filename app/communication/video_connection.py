from communication.video_client import VideoClient

class VideoConnection:
    def __init__(self, host, port, exit_flag, img_queue):
        self.host = host
        self.port = port
        self.exit_flag = exit_flag
        self.img_queue = img_queue

    def start(self):
        self.exit_flag.clear()
        vc = VideoClient(self.img_queue, self.exit_flag, self.host, self.port)
        vc.daemon = True
        vc.start()

    def stop(self):
        self.exit_flag.set()
