from threading import Thread
from threading import Event
from functools import reduce
import pandas as pd
import queue
import time

class DataSaver(Thread):
    def __init__(self, data_queue: queue.Queue, exit_flag: Event):
        Thread.__init__(self)
        self.data_queue = data_queue
        self.is_initial_save = True
        self.exit_flag = exit_flag
        self.columns_names = []
        self.file_name = None

    def run(self):
        print("[STARTED] DataSaver")
        while not self.exit_flag.is_set():
            try:
                data = self.data_queue.get()
                self._handle_data(data)
                self.data_queue.task_done()
            except queue.Empty as e:
                pass
        print("[STOPPED] DataSaver")

    def _handle_data(self, data):
        if self.is_initial_save:
            self._save_initial_data(data)
        else:
            self._save_data(data)

    def _extract_names(self, payload):
        return [data["name"] for data in payload["payload_data"]]

    def _extract_values(self, payload):
        return [data["value"] for data in payload["payload_data"]]
                
    def _save_initial_data(self, payload):
        self.file_name = "./tmp/" + time.strftime("%d%m%y-%H%M%S") + ".csv"
        self.columns_names = self._extract_names(payload)
        values = self._extract_values(payload)
        df = pd.DataFrame(data=[values], columns=self.columns_names)
        df.to_csv(self.file_name, index=False)
        self.is_initial_save = False

    def _save_data(self, payload):
        values = self._extract_values(payload)
        df = pd.DataFrame(data=[values], columns=self.columns_names)
        df.to_csv(self.file_name, mode='a', header=False, index=False)

    def _list_to_dict(self, data):
        temp_list = [{d["name"]:d["value"]} for d in data["payload_data"]]
        return reduce(lambda a, b: {**a, **b}, temp_list)   