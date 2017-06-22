import threading
from queue import Queue
import time


class Test:
    def __init__(self, queue):
        self.queue = queue
        self.thread = threading.Thread(target=self.run, name="queue_waiter")
        self.thread.start()

    def run(self):
        # print(self.queue.get(block=True))
        with self.queue.not_empty:
            self.queue.not_empty.wait()
        print(self.queue.get())


if __name__ == "__main__":
    t = Test(Queue())
    time.sleep(1)
    t.queue.put("hello")
    print("added item to the queue")

    while not t.queue.empty():
        print('waiting for queue to be processed')
        time.sleep(3)
