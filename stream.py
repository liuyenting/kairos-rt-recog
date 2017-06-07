# stream.py
#
# WebcamVideoStream
#   Encompass the actual camera acquisition thread. All the frames are pushed
#   into a ring buffer for retrieval.
#
# Reference
# ---------
# http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-
# opencv/

from threading import Thread
import cv2
from rbuf import RingBuffer

class WebcamVideoStream:
    def __init__(self, src=0):
        """
        Init the video camera, the ring buffer and read the first frame.
        """
        self._buffer = RingBuffer()

        self.stream = cv2.VideoCapture(src)
        #(_, frame) = self.stream.read()
        #self._buffer.push(frame)

        # variable used to indicate if the thread should be stopped
        self._stopped = False

    def start(self):
        """
        Start the thread to read frames from the video stream.
        """
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """
        Keep looping infinitely until the thread is stopped.
        """
        while not self._stopped:
            # read the next frame from the stream
            (_, frame) = self.stream.read()
            # push into the buffer
            self._buffer.push(frame)

    def read(self, block=True):
        """
        Return the frame most recently read.
        """
        while True:
            try:
                return self._buffer.pop()
            except IndexError:
                if not block:
                    return None

    def stop(self):
        """
        Indicate that the thread should be stopped.
        """
        self._stopped = True

    def __exit__(self, type, value, traceback):
        """
        Release the camera resource.
        """
        self.stream.release()
