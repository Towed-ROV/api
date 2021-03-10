from communication.sensor_subscriber import SensorSubscriber
from communication.data_saver_connection import DataSaverConnection
from sse_starlette.sse import EventSourceResponse
from schemas.sensor import Sensor
from pydantic import BaseModel
from fastapi import APIRouter, Request
import queue
import asyncio
import threading
import json
import time

router = APIRouter()
sensor_queue = queue.Queue()
sensor_sub = SensorSubscriber(sensor_queue, host="192.168.1.118", port=8001)
sensor_sub.setDaemon(True)
sensor_sub.start()

save_queue = None
exit_flag = threading.Event()
saver_connction = DataSaverConnection()
is_recording = False

# @router.get("/toggle_record")
# async def toggle_record():
#     global is_recording
#     global data_saver
#     is_recording = not is_recording

#     if is_recording:
#         exit_flag.clear()
#         data_saver = DataSaver(data_queue=data_queue, exit_flag=exit_flag)
#         data_saver.setDaemon(True)
#         data_saver.start()
#     else:
#         exit_flag.set()
#         data_queue.queue.clear()
#     return {"is_recording": is_recording}

@router.get("/toggle_recording")
def toggle_recording():
    global is_recording
    global save_queue

    is_recording = not is_recording
    
    if is_recording:
        save_queue = queue.Queue()
        saver_connction.start(save_queue, exit_flag)
    else:
        saver_connction.stop(save_queue, exit_flag)

    return {"is_recording": is_recording}


@router.get('/data')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        prev_data = "INIT"
        global is_recording
        while True:
            if await request.is_disconnected():
                break
            await asyncio.sleep(0.05) # TODO: Checkout tunings, freewheeling is troublebound
            try:
                data = sensor_queue.get(block=False) #
                if is_recording:
                    try:
                        save_queue.put_nowait(data)
                    except queue.Full:
                        print("full ..")
            except queue.Empty:
                data = prev_data
            yield {"event": "data", "data": json.dumps(data)}
            prev_data = data
    return EventSourceResponse(sensor_data_generator())