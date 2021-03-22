from communication.sensor_subscriber import SensorSubscriber
from communication.data_saver_connection import DataSaverConnection
from sse_starlette.sse import EventSourceResponse
from schemas.sensor import Sensor
from pydantic import BaseModel
from fastapi import APIRouter, Request, WebSocket
from multiprocessing import Pipe, Event
import queue
import asyncio
import threading
import json
import time

import random
from starlette.websockets import WebSocketDisconnect

router = APIRouter()
recv_q, send_q = Pipe(duplex=False)
sensor_sub = SensorSubscriber(send_q, host="192.168.1.118", port=8001)
sensor_sub.start()

save_queue = None
exit_flag = threading.Event()
saver_connction = DataSaverConnection()
is_recording = False

@router.get("/toggle_recording")
def toggle_recording():
    global is_recording
    global save_queue
    is_recording = not is_recording
    if is_recording:
        save_queue = queue.Queue() # enforce new queue everytime cus of slow garbage collection or something
        saver_connction.start(save_queue, exit_flag)
    else:
        saver_connction.stop(save_queue, exit_flag)
    return {"is_recording": is_recording}

@router.get('/stream')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        prev_data = {"payload_name": "default", "payload_data": []}
        global is_recording
        print("[OPEN] SSE")
        while True:
            if await request.is_disconnected():
                break
            await asyncio.sleep(0.01) # TODO: Checkout tunings, freewheeling is troublebound
            if recv_q.poll(0.01):
                data = recv_q.recv() #
                if is_recording: _save(data)
            else:
                data = prev_data
            yield {"event": "stream", "data": json.dumps(data)}
        print("[CLOSE] SSE")
    return EventSourceResponse(sensor_data_generator())

def _save(data):
    try:
        save_queue.put_nowait(data)
    except queue.Full:
        print("Full ..")

# @router.websocket("/ws/sensor")
# async def websocket_endpoint(websocket: WebSocket):
#     print("[STARTED] WS Sensor")
#     await websocket.accept()
#     global is_recording
#     while True:
#         try:
#             try:
#                 data = sensor_queue.get(block=False)
#                 if is_recording: _save(data)
#                 await websocket.send_json(data)
#             except queue.Empty:
#                 pass
#             await asyncio.sleep(0.01)
#         except Exception as e:
#             print('error:', e)
#             break
#     print('Bye..')
    

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             if recv_q.poll(0):
#                 data = recv_q.recv()
#                 if is_recording: _save(data)
#                 await manager.broadcast_json(data)
#             await asyncio.sleep(0.01)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         print("WS Closed.")

# def _save(data):
#     try:
#         save_queue.put_nowait(data)
#     except queue.Full:
#         print("Full ..")


