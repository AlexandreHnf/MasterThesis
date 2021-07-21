import time


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.timing_sec = 0
        self.timing_min = []  # [min, sec]
        self.elapsed_time_sec = ""
        self.elapsed_time_min = ""

    def convertSecToMin(self, seconds):
        minutes = seconds // 60
        sec = seconds - minutes * 60
        return minutes, sec

    def end_timer(self):
        """
        End the timer, and compute time elapsed in seconds and in minutes
        """
        self.end_time = time.time() - self.start_time
        self.timing_sec = self.end_time
        # self.elapsed_time_sec = f"{self.end_time} sec"
        self.elapsed_time_sec = "{0} sec".format(self.end_time)

        minutes, sec = self.convertSecToMin(self.end_time)
        self.timing_min = [minutes, sec]
        # self.elapsed_time_min = f"{minutes} min. {sec} sec"
        self.elapsed_time_min = "{0} min. {1} sec.".format(minutes, sec)

    def getTimeElapsedSec(self):
        """
        Precondition : first use end_timer
        """
        return self.timing_sec

    def getTimeElapsedMin(self):
        """
        Precondition : first use end_timer
        """
        return self.timing_min

    def getTimeElapsedSecTxt(self):
        """
        Precondition : first use end_timer
        """
        return self.elapsed_time_sec

    def getTimeElapsedMinTxt(self):
        """
        Precondition : first use end_timer
        """
        return self.elapsed_time_min

    def printTimeElapsedSec(self, name):
        if not self.end_time:
            self.end_timer()

        # print(f"{name} done in {self.elapsed_time_sec}")
        print("{0} done in {1}".format(name, self.elapsed_time_sec))

    def printTimeElapsedMin(self, name):
        if not self.end_time:
            self.end_timer()

        # print(f"{name} done in {self.elapsed_time_min}")
        print("{0} done in {1}".format(name, self.elapsed_time_min))
