# WebcamVideoStream
#
# Encompass the actual camera acquisition thread.
#
# Reference
# ---------
# https://codereview.stackexchange.com/questions/85068/efficient-ring-buffer-fifo

import collections
import itertools

class RingBuffer(object):
    def __init__ (self, size=16):
            self._buffer = collections.deque(maxlen=size)

    def push(self, data):
            """
            Adds data to the end of the buffer.
            """
            self._buffer.append(data)

    def pop(self):
            """
            Retrieves data from the beginning of the buffer.
            """
            if len(self):
                return self._buffer.popleft()
            else:
                raise IndexError('Buffer is empty')

    def snapshot(self):
        return list(self._buffer)

    def __len__(self):
            """
            Returns the length of the buffer.
            """
            return len(self._buffer)
