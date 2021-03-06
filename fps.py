# FPS
#
# Used to approximate frames per second of a give camera and computer vision
# processing pipeline.
#
# Reference
# ---------
# http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-
# opencv/

import datetime

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._nFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._nFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        #TODO: modify to allow continuous query
        return self._nFrames / self.elapsed()
