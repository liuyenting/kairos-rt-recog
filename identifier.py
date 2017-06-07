# identifier.py
#
# FaceIdentifier
#   Identify possible faces in the image.
#
# NameIdentifier
#   Send the image to Kairos in order to identify its possible name.

from __future__ import print_function
import cv2
from PIL import Image
from ConfigParser import ConfigParser
import cStringIO
import base64
import requests

class FaceIdentifier:
    def __init__(self, path):
        print('[INFO] loading pre-trained "%s"' % (path))
        self._classifier = cv2.CascadeClassifier(path)

        # ROI boundary box
        self.minSize = (50, 50)

    def findFaces(self, image):
        """
        Find all possible faces in the provided RGB image.
        """
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
        """
        Draw ROIs on the supplied background image.
        """
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
        config = ConfigParser()
        config.read(path)

        # load the credentials
        appId = config.get('Kairos', 'AppId')
        appKey = config.get('Kairos', 'AppKey')

        # preset the POST header
        self._headers = {
            'Content-Type': 'application/json',
            'app_id': appId,
            'app_key': appKey
        }

    def identify(self, face):
        # create buffer for faces
        self._buffer = cStringIO.StringIO()

        # acquire Image object
        imgObj = Image.fromarray(face, 'RGB')
        # dump to the buffer as PNG
        imgObj.save(self._buffer, format='PNG')

        # encode to base64 for transfer
        imgStr = base64.b64encode(self._buffer.getvalue())

        # generate the post fields
        values = {
            'image': 'data:image/png;base64,' + imgStr,
            'gallery_name': 'AKB48'
        }
        # send the request
        response = requests.post(
            'https://api.kairos.com/recognize',
            headers=self._headers,
            json=values
        )

        # close object and discard memory buffer
        self._buffer.close()

        # parse the JSON result
        result = json.loads(response.text)
        # return the name
        if 'images' in result:
            result = result['images'][0]['transaction']
            if 'subject_id' in result:
                return result['subject_id']
        else:
            return None
