from fastapi import APIRouter
from pydantic import BaseModel
from threading import Event
from queue import Queue
from starlette.responses import StreamingResponse
from communication.video_connection import VideoConnection
import cv2

router = APIRouter()

img_queue = Queue()
exit_flag = Event()
video_connection = VideoConnection(exit_flag, img_queue)

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
    img = img_queue.get()
    cv2.imwrite("./tmp/test_image.jpg", img)
    img_queue.task_done()

@router.get("/video")
async def frame_streamer():
    def frame_generator():
        while True:
            img = img_queue.get()
            _, frame_buffer = cv2.imencode('.jpg', img)
            frame_bytes = frame_buffer.tobytes()
            yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
            img_queue.task_done()
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

