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
from rbuf import RingBuffer
from ConfigParser import ConfigParser
from threading import Thread
import cStringIO
import base64
import requests
import json
from datetime import datetime

class FaceIdentifier:
    def __init__(self, path):
        print('[INFO] loading pre-trained "%s"' % (path))
        self._classifier = cv2.CascadeClassifier(path)

        # ROI boundary box
        self.minSize = (100, 100)

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

class KairosResponse:
    SUCCESS, UNKNOWN, NO_FACE = range(3)

class NameIdentifier:
    def __init__(self, path):
        config = ConfigParser()
        config.read(path)

        # load the credentials
        appId = config.get('Kairos', 'AppId')
        appKey = config.get('Kairos', 'AppKey')
        # load the templates
        self._gallery = config.get('Kairos', 'Gallery')

        print('[DEBUG] AppId = [%s]' % (appId))
        print('[DEBUG] AppKey = [%s]' % (appKey))

        # preset the POST header
        self._headers = {
            'Content-Type': 'application/json',
            'app_id': appId,
            'app_key': appKey
        }

        self._buffer = RingBuffer(size=2)
        # variable used to indicate if the thread should be stopped
        self._stopped = False

    def start(self):
        """
        Start the identification service.
        """
        Thread(target=self.worker, args=()).start()
        return self

    def queryID(self, face):
        """
        Query the student ID for specified face.
        """
        self._buffer.push(face)

    def worker(self):
        """
        Keep pop out the face from buffer.
        """
        while not self._stopped:
            try:
                # pop a new face
                face = self._buffer.pop()

                # ask Kairos
                state, sid = self._identify(face)
                if state == KairosResponse.SUCCESS:
                    # send to the signup sheet server
                    response = requests.post(
                        'http://172.16.217.90/signup.php',
                        data={'student_id': sid}
                    )
                    sid = '[' + sid + ']'
                elif state == KairosResponse.NO_FACE:
                    sid = '<no face>'
                elif state == KairosResponse.UNKNOWN:
                    sid = '<unknown>'

                print('%s %s' % (str(datetime.now()), sid))
            except IndexError:
                pass

    def _identify(self, face):
        # create buffer for faces
        fileBuf = cStringIO.StringIO()

        # acquire Image object
        imgObj = Image.fromarray(face, 'RGB')
        # dump to the buffer as PNG
        imgObj.save(fileBuf, format='PNG')

        # encode to base64 for transfer
        imgStr = base64.b64encode(fileBuf.getvalue())

        # generate the post fields
        values = {
            'image': 'data:image/png;base64,' + imgStr,
            'gallery_name': self._gallery
        }
        # send the request
        response = requests.post(
            'https://api.kairos.com/recognize',
            headers=self._headers,
            json=values
        )

        # close object and discard memory buffer
        fileBuf.close()

        # parse the JSON result
        result = json.loads(response.text)

        # return the name
        sid = None
        state = None
        if 'images' in result:
            result = result['images'][0]['transaction']
            if 'subject_id' in result:
                state = KairosResponse.SUCCESS
                sid = result['subject_id']
            else:
                state = KairosResponse.UNKNOWN
        else:
            state = KairosResponse.NO_FACE
        return (state, sid)

    def stop(self):
        """
        Stop the query thread.
        """
        self._stopped = True
