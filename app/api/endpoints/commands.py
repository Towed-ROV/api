from queue import Queue

from communication.command_dispatcher import CommandDispatcher
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from schemas.command import Command

router = APIRouter()
command_queue = Queue()

dispatcher = CommandDispatcher(command_queue, host="192.168.1.118", port=7001)
dispatcher.setDaemon(True)
# dispatcher.start()


@router.post("/")
def post_cmd(cmd: Command):
    print("CMD: ", cmd)
    if cmd.toSystem:
        cmd.value = bool(cmd.value)
    payload = {
        "payload_name": "commands",
        "payload_data":  [{
            "name": cmd.name,
            "value": cmd.value
        }]
    }
    command_queue.put(payload)
    print(payload)
    return {"code": "success", "sent": payload}


""" 
One could actually use the send / recv directly in the command-endpoints,
therby redirecting the response received from the socket
as a response to the post-endpoint is called
"""
