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
            self._buffer.extend(data)

    def pop(self, size=1):
            """
            Retrieves data from the beginning of the buffer.
            """
            if size > len(self._buffer):
                raise IndexError(
                    "Too many items: trying to access %d items from a buffer "
                    "of length %d" % (size, len(self))
                )
            data = [self._buffer.popleft() for _ in xrange(size)]
            return data

    def peek(self, size=1):
            """
            Peek at the beginning of the buffer.
            """
            return str(bytearray(itertools.islice(self._buffer, size)))

    def length(self):
            """
            Returns the length of the buffer.
            """
            return len(self._buffer)
