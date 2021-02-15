import asyncio
import queue
import time
import cv2
import zmq
import threading

# MODULES
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Body
from starlette.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from communication.command_dispatcher import CommandDispatcher
from communication.sensor_subscriber import SensorSubscriber
from communication.video_client import VideoClient

from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from fastapi.openapi.models import Response
from fastapi.encoders import jsonable_encoder

# SERVER SETTINGS / PATHS
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

cmd_queue = queue.Queue()
sen_queue = queue.Queue()
cd = CommandDispatcher(cmd_queue, host="192.168.1.118", port=7001)
ss = SensorSubscriber(sen_queue, host="192.168.1.118", port=8001)
cd.setDaemon(True)
ss.setDaemon(True)
cd.start()
ss.start()

img_queue = queue.Queue(maxsize=30)
vc = VideoClient(img_queue, "192.168.1.118", 1337)
vc.setDaemon(True)
vc.start()


class Command(BaseModel):
    name: str
    value: float

@app.get("/")
def root():
    return "Welcome"

@app.post("/command")
async def post_cmd(cmd: Command):
    c = jsonable_encoder(cmd)
    cmd_queue.put(c)
    return cmd

@app.get('/sensor_data')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        prev_data = "INIT"
        while True:
            if await request.is_disconnected():
                break
            try:
                data = sen_queue.get(block=False)
            except queue.Empty:
                data = prev_data
            yield {
                    "event": "data",
                    "data": data,
            }
            prev_data = data
    return EventSourceResponse(sensor_data_generator())

def frame_generator():
    while True:
        img = img_queue.get()
        _, frame_buffer = cv2.imencode('.jpg', img)
        frame_bytes = frame_buffer.tobytes()
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
        img_queue.task_done()

@app.get("/video")
async def frame_streamer():
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

