from communication.video_connection import VideoConnection
from communication.sonar_connection import SonarConnection
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter
from multiprocessing import Queue, Event
import queue
import cv2

router = APIRouter()


exit_flag = Event()
img_queue = Queue(maxsize=30)

video_connection = VideoConnection("192.168.1.118", 1337, img_queue, exit_flag)
sonar_connection = SonarConnection("127.0.0.1", 5555, img_queue)

TYPE_VIDEO = "VIDEO"
TYPE_SONAR = "SONAR"
DISPLAY_TYPE = TYPE_VIDEO # DEFAULT

TEST_IMAGE = "./tmp/test.png"
TMP_FOLDER = "./tmp/"
IMAGE_FOLDER = "./images/"

def save_img():
    # img = img_queue.get()
    img = cv2.imread(TEST_IMAGE)
    img_name = datetime.now().strftime("%d-%m-%Y %H_%M_%S.%f")[:-4]
    img_name += ".jpg"
    file_name = IMAGE_FOLDER + img_name
    cv2.imwrite(file_name, img)
    return img_name

@router.post("display/{display_mode}")
def set_type(display_mode: str):
    global DISPLAY_TYPE
    success = False
    if display_mode == TYPE_VIDEO or display_mode == TYPE_VIDEO:
        DISPLAY_TYPE = display_mode
        success = True
    else:
        # raise errors
        pass
    return {"code": success}

@router.get("/start")
def video_start():
    global img_queue
    if TYPE_VIDEO == TYPE_VIDEO: video_connection.start()
    if TYPE_VIDEO == TYPE_SONAR: sonar_connection.start()
    return {"code": "success!"}

@router.get("/stop")
def video_stop():
    if TYPE_VIDEO == TYPE_VIDEO: video_connection.stop()
    if TYPE_VIDEO == TYPE_SONAR: sonar_connection.stop()
    return {"code": "success!"}

@router.get("/snap")
def video_snapshot():
    try:
        img = img_queue.get()
        img_name = datetime.now().strftime("%d-%m-%Y %H_%M_%S.%f")[:-4]
        img_name += ".jpg"
        file_name = TMP_FOLDER + img_name
        cv2.imwrite(file_name, img)
        succeeded = True
    except queue.Empty:
        succeeded = False
    return {"succeeded": succeeded, "img_name": img_name}

@router.get("/live")
async def frame_streamer():
    def frame_generator():
        while True:
            try:
                img = img_queue.get(0.01)
                _, frame_buffer = cv2.imencode('.jpg', img)
                frame_bytes = frame_buffer.tobytes()
                yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
            except queue.Empty:
                pass
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/{img_name}")
def get_img_from_database(img_name: str):
    return FileResponse(IMAGE_FOLDER + img_name)



