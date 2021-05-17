import time


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None

    def end_timer(self):
        self.end_time = time.time() - self.start_time

    def getTimeElapsedSec(self):
        return self.end_time

    def printTimeElapsedSec(self, name):
        if not self.end_time:
            self.end_timer()
        print(f"{name} done in {self.end_time} sec.")

    def printTimeElapsedMin(self, name):
        if not self.end_time:
            self.end_timer()
        minutes = self.end_time // 60
        seconds = self.end_time - minutes*60

        print(f"{name} done in {minutes} min. {seconds} sec.")
