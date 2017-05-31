import cv2      # opencv
import numpy
from PIL import Image
from tempfile import NamedTemporaryFile as ntmpf
import base64
import requests
import json
import os
import sys      # system calls
import time

url = 'https://api.kairos.com/recognize';
appId = '420de94a';
appKey = 'bb9d4e85c8acbb16de74654e4a9c009a';

headers = {
    'Content-Type': 'application/json',
    'app_id': appId,
    'app_key': appKey
}

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # slice the ROI
        face = frame[y:y+h, x:x+w]

        # to image object
        result = Image.fromarray(face, 'RGB')

        # create temp file
        f = ntmpf(dir='.', suffix='.png', delete=False)
        fname = f.name

        # save to temp file
        result.save(fname);

        # dump file as base64 string
        with open(fname, 'rb') as f:
            imstr = base64.b64encode(f.read())

        # unlink
        f.close()

        # generate the post fields
        values = {
            'image': 'data:image/png;base64,' + imstr,
            'gallery_name': 'AKB48'
        }

        # send the request
        response = requests.post(url, headers=headers, json=values)

        # convert to json string
        result = json.dumps(json.loads(response.text), indent=3)
        # print result
        print result + '\n'

    # display the resulting frame
    cv2.imshow('Video', frame)

    time.sleep(2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
