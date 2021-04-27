import copy
import queue
import time
from functools import reduce
from threading import Event, Thread

import pandas as pd


class DataSaver(Thread):
    def __init__(self, data_queue: queue.Queue, exit_flag: Event):
        """This class is tailored to act as a CSV-writer.
        Will handle all logic considering filenames,
        initial save and adding to exisiting file.

        Args:
            data_queue (queue.Queue): message queue for the incoming sensordata
            exit_flag (threading.Event): exit-flag for opting out of the thread
        """
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
                payload = self.data_queue.get()
                payload_copy = copy.deepcopy(payload) # So we can mutate without changing original
                payload_copy["payload_data"].insert(0, {"name": "timestamp", "value": time.time()})
                self._handle_save_data(payload_copy)
                self.data_queue.task_done()
            except queue.Empty:
                pass
        print("[STOPPED] DataSaver")

    def _handle_save_data(self, data):
        if self.is_initial_save:
            self._save_initial_data(data)
        else:
            self._save_data(data)
                
    def _save_initial_data(self, payload):
        """method for initializin the CSV-file and writes the header row

        Args:
            payload (dict): the sensordata
        """
        self.file_name = "./tmp/" + time.strftime("%d%m%y-%H%M%S") + ".csv"
        self.columns_names = DataSaver.extract_names(payload) # header names
        values = DataSaver.extract_values(payload)            # corresponding values
        df = pd.DataFrame(data=[values], columns=self.columns_names)
        df.to_csv(self.file_name, index=False)
        self.is_initial_save = False

    def _save_data(self, payload):
        """method used after initial save, just adds to an exisisting csv-file

        Args:
            payload (dict): the sensordata
        """
        values = DataSaver.extract_values(payload)
        df = pd.DataFrame(data=[values], columns=self.columns_names)
        df.to_csv(self.file_name, mode='a', header=False, index=False)
    
    @staticmethod
    def extract_names(payload):
        return [data["name"] for data in payload["payload_data"]]

    @staticmethod
    def extract_values(payload):
        items = []
        last_item = None
        try:
            for data in payload["payload_data"]:
                last_item = data
                items.append(data["value"])
        except Exception as e:
            print("ERROR ITEM: ", str(last_item))
            print(e)
        return items
    
    @staticmethod
    def list_to_dict(data):
        temp_list = [{d["name"]:d["value"]} for d in data["payload_data"]]
        return reduce(lambda a, b: {**a, **b}, temp_list)   
