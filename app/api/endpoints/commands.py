from communication.command_dispatcher import CommandDispatcher
from schemas.command import Command
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import APIRouter
from queue import Queue
import zmq

router = APIRouter()
command_queue = Queue()
dispatcher = CommandDispatcher(command_queue, host="192.168.1.118", port=7001)
dispatcher.setDaemon(True)
dispatcher.start()

@router.post("/cmd")
def post_cmd(cmd: Command):
    command = jsonable_encoder(cmd)
    command_queue.put(command)
    return {"code": "success", "sent": command}

""" 
One could actually use the send / recv directly in the command-endpoints,
therby redirecting the response received from the socket
as a response to the post-endpoint is called
"""