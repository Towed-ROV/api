from communication.command_client import CommandClient

c = CommandClient(host="127.0.0.1", port=2626)
c.start()