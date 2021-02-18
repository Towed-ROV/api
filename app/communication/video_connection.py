from communication.video_client import VideoClient

class VideoConnection:
    def __init__(self, exit_flag, img_queue):
        self.exit_flag = exit_flag
        self.img_queue = img_queue

    def start(self):
        self.exit_flag.clear()
        vc = VideoClient(self.img_queue, self.exit_flag, "192.168.1.118", 1337)
        vc.setDaemon(True)
        vc.start()

    def stop(self):
        self.exit_flag.set()
        self.img_queue.queue.clear()

        