from communication.sensor_subscriber import SensorSubscriber
from communication.data_saver_connection import DataSaverConnection
from communication.payload_receiver import PayloadReceiver
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request
from multiprocessing import Queue
import time
import queue
import asyncio
import threading
import json

router = APIRouter()

# 
data_queue_1 = Queue(maxsize=15)
sensor_sub = SensorSubscriber(data_queue_1, host="192.168.1.118", port=8001)
sensor_sub.start()

data_queue_2 = Queue(maxsize=15)
sensor_sub = SensorSubscriber(data_queue_2, host="192.168.1.118", port=8002)
sensor_sub.start()

payload_receiver = PayloadReceiver()
payload_receiver.add_queue(data_queue_1)
payload_receiver.add_queue(data_queue_2)

save_queue = None
is_recording = False
exit_flag = threading.Event()
saver_connection = DataSaverConnection()

@router.get("/toggle_recording")
def toggle_recording():
    global is_recording
    global save_queue
    is_recording = not is_recording
    if is_recording:
        save_queue = queue.Queue() # enforce new queue everytime cus of slow garbage collection or something
        saver_connection.start(save_queue, exit_flag)
    else:
        saver_connection.stop(save_queue, exit_flag)
        save_queue = None
    return {"is_recording": is_recording}

@router.get('/stream')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        print("[OPEN] SSE")
        global is_recording
        skips = 0
        counter_skip = 0
        counter_sent = 0
        start = time.time()
        while True:
            if await request.is_disconnected():
                break
            payload = payload_receiver.get_all()
            if payload is not None:
                if is_recording: _save(payload)
                yield {"event": "stream", "data": json.dumps(payload)}
                counter_sent = counter_sent + 1
            else:
                counter_skip = counter_skip + 1
            
            # DEBUGG HELP
            if ((time.time() - start) > 5):
                print("TIME________: ", str(time.time() - start))
                print("Times sent  : ", str(counter_sent))
                print("Times skips : ", str(counter_skip))
                counter_sent = 0
                counter_skip = 0
                start = time.time()
            await asyncio.sleep(0.09)
                
        print("SKIPS: ", str(skips))
        print("[CLOSE] SSE")
    return EventSourceResponse(sensor_data_generator())


""" ___________________________HELPERS________________________________ """

def _save(payload):
    if payload is None:
        return
    if payload["payload_name"] == "sensor_data":
        try:
            save_queue.put_nowait(payload)
        except queue.Full:
            print("FULL QUEUE")

