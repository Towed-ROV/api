from communication.data_saver import DataSaver


class DataSaverConnection:
    """ connector between the endpoint requests and the actual local data writer """
    def __init__(self):
        pass

    def start(self, que, flag):
        """initializes the csv writer

        Args:
            que (queue.Queue): sensordata queue
            flag ([queue.Event): exit-flag to opt out / clean up / exit
        """
        flag.clear()
        vc = DataSaver(que, flag)
        vc.setDaemon(True)
        vc.start()

    def stop(self, que, flag):
        flag.set()
        que.queue.clear()

        