from communication.command_dispatcher import CommandDispatcher
from schemas.command import Command
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import APIRouter
from queue import Queue
import zmq

router = APIRouter()
command_queue = Queue()
dispatcher = CommandDispatcher(command_queue, host="192.168.0.102", port=8764)
dispatcher.setDaemon(True)
dispatcher.start()

@router.post("/")
def post_cmd(cmd: Command):
    command = jsonable_encoder(cmd)
    if command["toSystem"]:
        command["value"] = bool(command["value"])
    payload = {
        "payload_name": "commands",
        "payload_data":  [{
            "name": command["name"],
            "value": command["value"]
        }]
    }
    command_queue.put(payload)
    return {"code": "success", "sent": payload}

""" 
One could actually use the send / recv directly in the command-endpoints,
therby redirecting the response received from the socket
as a response to the post-endpoint is called
"""