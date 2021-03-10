from communication.data_saver import DataSaver

class DataSaverConnection:
    def __init__(self):
        pass

    def start(self, que, flag):
        flag.clear()
        vc = DataSaver(que, flag)
        vc.setDaemon(True)
        vc.start()

    def stop(self, que, flag):
        flag.set()
        que.queue.clear()

        