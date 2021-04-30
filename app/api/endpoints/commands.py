from queue import Queue

from communication.command_dispatcher import CommandDispatcher
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from schemas.command import Command

router = APIRouter()
command_queue = Queue()

dispatcher = CommandDispatcher(command_queue, host="192.168.1.118", port=7001)
dispatcher.setDaemon(True)
dispatcher.start()


@router.post("/")
def send_command_to_rov(cmd: Command):
    """Accepts a command-payload, and adds it
    to a command dispatcher, which sends the command through ZMQ
    to the ROV.

    Args:
        cmd (Command): command payload

    Returns:
        dict: success details
    """
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
    return {"code": "success", "sent": payload}
