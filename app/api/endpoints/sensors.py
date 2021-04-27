import asyncio
import json
import queue
import threading
import time
from multiprocessing import Queue

from communication.data_saver_connection import DataSaverConnection
from communication.payload_receiver import PayloadReceiver
from communication.sensor_subscriber import SensorSubscriber
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

router = APIRouter()

# FROM THE REMOTE TOWED-ROV
data_queue_1 = Queue(maxsize=15)
sensor_sub = SensorSubscriber(data_queue_1, host="192.168.1.118", port=8001)
# sensor_sub.start()

# FROM THE LOCAL SUITCASE BOX
data_queue_2 = Queue(maxsize=15)
sensor_sub = SensorSubscriber(data_queue_2, host="192.168.1.118", port=8002)
# sensor_sub.start()

# COLLECTS DATA AND PROCESSES DATA FROM ALL PUBLISHERS
payload_receiver = PayloadReceiver()
payload_receiver.add_queue(data_queue_1)
payload_receiver.add_queue(data_queue_2)

# CONTROL ACCESS OBJECTS
save_queue = None
is_recording = False
exit_flag = threading.Event()
saver_connection = DataSaverConnection()


@router.get("/toggle_recording")
def toggle_recording():
    """starts recording the sensordata in csv""

    Returns:
        dict: wether the recording is running or not
    """
    global is_recording
    global save_queue
    is_recording = not is_recording
    if is_recording:
        # enforce new queue everytime (cus of slow garbage collection or something?)
        save_queue = queue.Queue()
        saver_connection.start(save_queue, exit_flag)
    else:
        saver_connection.stop(save_queue, exit_flag)
        save_queue = None
    return {"is_recording": is_recording}


@router.get('/live')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        """receives data through two ZMQ subscribers,
        and yields a EventSourceResponse for listeners to receive the sensordata stream

        Yields:
            EventSourceResponse: json payload containing the sensordata
        """
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
                if is_recording:
                    save_to_csv(payload)
                yield {"event": "stream", "data": json.dumps(payload)}
                counter_sent = counter_sent + 1
            else:
                counter_skip = counter_skip + 1

            # DEBUGG HELP
            # TODO: remove before production release
            if ((time.time() - start) > 5):
                print("TIME________: ", str(time.time() - start))
                print("Times sent  : ", str(counter_sent))
                print("Times skips : ", str(counter_skip))
                counter_sent = 0
                counter_skip = 0
                start = time.time()
            await asyncio.sleep(0.09)

        print("[CLOSE] SSE")
    return EventSourceResponse(sensor_data_generator())

def save_to_csv(payload):
    """Adds sensordata (payload) to a writer queue for saving

    Args:
        payload (dict): containing the sensordata
    """
    if payload is None:
        return

    # guard against not saving payloads with invalid name such as "response"-payloads
    if payload["payload_name"] == "sensor_data":
        try:
            save_queue.put_nowait(payload)
        except queue.Full:
            print("FULL QUEUE")
