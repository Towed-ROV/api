from app.communication.video_client import VideoClient
import cv2

def start_video_client(vq, ve):
    vc = VideoClient(vq, ve, "192.168.1.118", 1337)
    vc.setDaemon(True)
    vc.start()

def save_image(path, frame):
    cv2.imwrite(path, frame)