import queue
from datetime import datetime
from multiprocessing import Event, Queue

import cv2
from communication.sonar_connection import SonarConnection
from communication.video_connection import VideoConnection
from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemas.video_preference import VideoPreference
from starlette.responses import StreamingResponse

router = APIRouter()

# Video utils
exit_flag = Event()
img_queue = Queue(maxsize=30)
video_connection = VideoConnection("192.168.1.118", 1337, img_queue, exit_flag)
sonar_connection = SonarConnection("127.0.0.1", 5555, img_queue, exit_flag)

# Video state
S_DISPLAY_VIDEO = "video"
S_DISPLAY_SONAR = "sonar"
S_DISPLAY_TYPE = S_DISPLAY_VIDEO  # DEFAULT

# Video folders
TEST_IMAGE = "./tmp/test.png"
TMP_FOLDER = "./tmp/"
IMAGE_FOLDER = "./images/"


def save_img():
    """helper method for saving images in videos.py and in crud.py
    (used in crud.py)

    Returns:
        str: filename of the image saved 
    """
    img = img_queue.get()
    # img = cv2.imread(TEST_IMAGE) # If using seed-database in Settings-page
    img_name = datetime.now().strftime("%d-%m-%Y %H_%M_%S.%f")[:-4]
    img_name += ".jpg"
    file_name = IMAGE_FOLDER + img_name
    cv2.imwrite(file_name, img)
    return img_name


@router.post("/preference")
def video_preference(video_preference: VideoPreference):
    """Control method for toggle start/stop between streaming
    the video-feed from the camera or the side scan sonar

    Args:
        video_preference (VideoPreference): basemodel for video preference

    Returns:
        dict: containing local state and wether if request was successfull
    """
    global S_DISPLAY_TYPE
    success = False
    action = video_preference.action              # START / STOP
    display_mode = video_preference.display_mode  # VIDEO / SONAR
    print(video_preference)
    if action == "start":
        if display_mode == S_DISPLAY_VIDEO:
            S_DISPLAY_TYPE = S_DISPLAY_VIDEO
            video_connection.start()
            success = True
        elif display_mode == S_DISPLAY_SONAR:
            S_DISPLAY_TYPE = S_DISPLAY_SONAR
            sonar_connection.start()
            success = True

    elif action == "stop":
        if display_mode == S_DISPLAY_VIDEO:
            video_connection.stop()
            success = True
            S_DISPLAY_TYPE = None
        elif display_mode == S_DISPLAY_SONAR:
            sonar_connection.stop()
            success = True
            S_DISPLAY_TYPE = None

    return {"success": success, "preference": {"action": action, "display_mode": display_mode}}


@router.get("/snap")
def trigger_image_snapshot():
    """Store a snapshot of the moment the button was clicked,
    save either a side-scan-sonar image or a camera-photo

    Returns:
        dict: containing success info
    """
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
    """Livestream pipeline for receving the video-feed from the sonar / camera

    Yields: streams the response body with the encoded image buffer
    """
    global S_DISPLAY_SONAR

    def frame_generator():
        while True:
            try:
                img = img_queue.get(0.01)
                if S_DISPLAY_SONAR:
                    img = cv2.resize(img, (640, 480))
                _, frame_buffer = cv2.imencode('.jpg', img)
                frame_bytes = frame_buffer.tobytes()
                yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
            except queue.Empty:
                pass
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/{img_name}")
def get_img_from_database(img_name: str):
    """Retrieves a image from the database,
    specified by the param filename 

    Args:
        img_name (str): the filename of the image in database

    Returns:
        FileResponse: asynchronously streams a file as the response
    """
    return FileResponse(IMAGE_FOLDER + img_name)
