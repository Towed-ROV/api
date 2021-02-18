from communication.sensor_subscriber import SensorSubscriber
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from fastapi import APIRouter, Request
import queue
import asyncio
import json

router = APIRouter()
sensor_queue = queue.Queue()
sensor_sub = SensorSubscriber(sensor_queue, host="192.168.1.118", port=8001)
sensor_sub.setDaemon(True)
sensor_sub.start()

@router.get('/data')
async def sensor_data(request: Request):
    async def sensor_data_generator():
        prev_data = "INIT"
        while True:
            if await request.is_disconnected():
                break
            await asyncio.sleep(0.05) # TODO: Checkout tunings
            try:
                data = sensor_queue.get(block=False) # non-blocking loop
            except queue.Empty:
                data = prev_data
            yield {"event": "data", "data": json.dumps(data)}
            prev_data = data
    return EventSourceResponse(sensor_data_generator())