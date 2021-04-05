from fastapi import APIRouter
from pydantic import BaseModel
from threading import Event
import queue
from multiprocessing import Event, Pipe, Queue
from starlette.responses import StreamingResponse
from communication.video_connection import VideoConnection
import cv2

router = APIRouter()
img_queue = Queue(maxsize=30)
exit_flag = Event()
video_connection = VideoConnection("192.168.1.118", 1337, exit_flag, img_queue)
is_save = False

@router.get("/video_start")
def video_start():
    video_connection.start()
    return {"code": "success!"}

@router.get("/video_stop")
def video_stop():
    video_connection.stop()
    return {"code": "success!"}

@router.get("/video_snapshot")
def video_snapshot():
    global is_save
    is_save = True
    return {"code": "success!"}

@router.get("/video")
async def frame_streamer():
    def frame_generator():
        global is_save
        while True:
            try:
                img = img_queue.get_nowait()
                if is_save: _save(img)
                _, frame_buffer = cv2.imencode('.jpg', img)
                frame_bytes = frame_buffer.tobytes()
                yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
            except queue.Empty:
                pass
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

def _save(img):
    global is_save
    if is_save:
        cv2.imwrite("./tmp/test_image.jpg", img)
        is_save = False

