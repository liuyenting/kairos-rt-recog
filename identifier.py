# identifier.py
#
# FaceIdentifier
#   Identify possible faces in the image.
#
# NameIdentifier
#   Send the image to Kairos in order to identify its possible name.

from __future__ import print_function
import cv2
from ConfigParser import ConfigParser

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

class NameIdentifier:
    def __init__(self, path):
        # parse config file to look for credentials
        config = ConfigParser()
        config.read(path)
