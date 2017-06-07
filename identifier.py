# WebcamVideoStream
#
# Encompass the actual camera acquisition thread. All the frames are pushed into
# a ring buffer for retrieval.
#
# Reference
# ---------
# http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-
# opencv/

from __future__ import print_function
import cv2

class FaceIdentifier:
    def __init__(self, path):
        print('[INFO] loading pre-trained "%s"' % (path))
        self._classifier = cv2.CascadeClassifier(path)

        # ROI boundary box
        self.minSize = (50, 50)

    def findFaces(self, image):
        # convert to grayscale for further processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # apply the cascade classifier
        faces = self._classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.minSize
        )
        return faces

    def drawROI(self, image, roi):
        # draw a rectangle around the faces
        for (x, y, w, h) in roi:
            cv2.rectangle(
                image,
                (x, y),         # lower left
                (x+w, y+h),     # upper right
                (0, 255, 0),    # border color
                2               # line thickness
            )
