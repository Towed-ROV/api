from communication.command_dispatcher import CommandDispatcher
from schemas.command import Command
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from queue import Queue

router = APIRouter()
command_queue = Queue()
dispatcher = CommandDispatcher(command_queue, host="192.168.0.110", port=8767)
dispatcher.setDaemon(True)
dispatcher.start()

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