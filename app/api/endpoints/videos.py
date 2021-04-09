from communication.video_connection import VideoConnection
from starlette.responses import StreamingResponse
from multiprocessing import Event, Queue
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter
from threading import Event
import queue
import cv2

router = APIRouter()

# img_queue = Queue(maxsize=30)
# exit_flag = Event()
# video_connection = VideoConnection("192.168.1.118", 1337, exit_flag, img_queue)
# is_save = False

TEST_IMAGE = "./tmp/480p.png"
IMAGE_FOLDER = "./images/"

def save_img():
    # global img_queue
    # img = img_queue.get()
    img = cv2.imread(TEST_IMAGE)
    img_name = datetime.now().strftime("%d-%m-%Y %H_%M_%S.%f")[:-4]
    img_name += ".jpg"
    file_name = IMAGE_FOLDER + img_name
    cv2.imwrite(file_name, img)
    return img_name

@router.get("/start")
def video_start():
    video_connection.start()
    return {"code": "success!"}

@router.get("/stop")
def video_stop():
    video_connection.stop()
    return {"code": "success!"}

@router.get("/snapshot")
def video_snapshot():
    try:
        img = img_queue.get(timeout=0.25)
        img_name = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")[:-4]
        cv2.imwrite(f"./tmp/{img_name}.jpg", img)
        succeeded = True
    except queue.Empty:
        succeeded = False
    return {"succeeded": succeeded, "img_name": img_name}

@router.get("/feed")
async def frame_streamer():
    def frame_generator():
        global is_save
        while True:
            try:
                img = img_queue.get_nowait()
                _, frame_buffer = cv2.imencode('.jpg', img)
                frame_bytes = frame_buffer.tobytes()
                yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
            except queue.Empty:
                pass
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")



