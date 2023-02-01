import threading
import time

class CenterCounter(threading.Thread):
    def __init__(self,counter):
        threading.Thread.__init__(self)
        self.counter =counter

    def run(self):
        self.printCounterText(self.counter)

    def printCounterText(self,counter):
        while self.counter > 0:
            time.sleep(1)
            self.counter -= 1



