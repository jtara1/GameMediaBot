import threading
import os
import json
from queue import Queue


class FileWriter:
    def __init__(self, file_name=os.path.join(os.getcwd(), 'last_ids.json')):
        self.queue = Queue()
        self.file_path = file_name

        if os.path.isfile(file_name):
            self.data_dict = json.load(open(file_name, 'r'))
        else:
            self.data_dict = {}

        self.thread = threading.Thread(target=self._write_queue, name="file_writer_queue_awaiter")
        self.thread.start()

    def write(self, data_dict):
        """ Sends dictionary to queue that'll be merged with the one
        in the file. It's not thread safe to update the dict value with the same key in
        more than one thread
        """
        self.data_dict.update(data_dict)  # update / merge the two dictionaries
        self.queue.put(self.data_dict)

    def _write_queue(self):
        while True:
            with self.queue.not_empty:
                self.queue.not_empty.wait()
            json.dump(self.data_dict, open(self.file_path, 'w'))  # save to file
