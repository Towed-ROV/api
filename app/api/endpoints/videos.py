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
sonar_connection = SonarConnection("127.0.0.1", 5555, img_queue, exit_flag)

S_DISPLAY_VIDEO = "video"
S_DISPLAY_SONAR = "sonar"
S_DISPLAY_TYPE = S_DISPLAY_VIDEO # DEFAULT

TEST_IMAGE = "./tmp/test.png"
TMP_FOLDER = "./tmp/"
IMAGE_FOLDER = "./images/"

class VideoPreference(BaseModel):
    action: str
    display_mode: str

def save_img():
    # img = img_queue.get()
    img = cv2.imread(TEST_IMAGE)
    img_name = datetime.now().strftime("%d-%m-%Y %H_%M_%S.%f")[:-4]
    img_name += ".jpg"
    file_name = IMAGE_FOLDER + img_name
    cv2.imwrite(file_name, img)
    return img_name

# @router.post("/{display_type}")
# def set_type(display_mode: str):
#     global S_DISPLAY_TYPE
#     success = False
#     if display_mode == S_DISPLAY_VIDEO or display_mode == S_DISPLAY_SONAR:
#         S_DISPLAY_TYPE = display_mode
#         success = True
#     return {"success": success, "type": S_DISPLAY_TYPE}

@router.post("/preference")
def video_preference(video_preference: VideoPreference):
    success = False
    action = video_preference.action
    display_mode = video_preference.display_mode
    if action == "start":
        if display_mode == S_DISPLAY_VIDEO:
            video_connection.start()
            success = True
        elif display_mode == S_DISPLAY_SONAR:
            sonar_connection.start()
            success = True
    elif action == "stop":
        if display_mode == S_DISPLAY_VIDEO:
            video_connection.stop()
            success = True
        elif display_mode == S_DISPLAY_SONAR:
            sonar_connection.stop()

            success = True
    return {"success": success, "preference": {"action": action, "display_mode": display_mode}}

# @router.get("/stop")
# def video_stop(video_preference: VideoPreference):
#     success = False
#     action = video_preference.action
#     mode = video_preference.display_mode
#     if mode == S_DISPLAY_VIDEO:
#         video_connection.stop()
#     elif mode == mode == S_DISPLAY_SONAR:
#         sonar_connection.stop()
#     else:
#         pass
#     return {"success": success, "display_mode": "XXXXXXX"}

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
async def live_video_feed():
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



