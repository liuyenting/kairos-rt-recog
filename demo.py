from __future__ import print_function
import argparse
from time import sleep
import cv2
from fps import FPS
from stream import WebcamVideoStream
from identifier import FaceIdentifier, NameIdentifier

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--display', action='store_true', default=False,
    help='Whether or not frames should be displayed'
)
parser.add_argument(
    '-c', '--classifier', default='haarcascade_frontalface_default.xml',
    help='Pre-trained cascade classifier definition'
)
args = vars(parser.parse_args())

cv2.namedWindow('Live Stream', cv2.WINDOW_NORMAL)

# identifiers
classifier = FaceIdentifier(args['classifier'])
kairos = NameIdentifier('jhopo_cred.ini').start()
# camera
stream = WebcamVideoStream(src=0).start()
fps = FPS().start()

while True:
    try:
        # grab a frame
        frame = stream.read(block=True)

        # analyze the faces
        faces = classifier.findFaces(frame)

        # crop the faces
        if faces is not None:
            for (x, y, w, h) in faces:
                # slice the ROI
                face = frame[y:y+h, x:x+w]
                # send to Kairos
                kairos.queryID(face)

        if args['display']:
            if faces is not None:
                classifier.drawROI(frame, faces)

            height, width = frame.shape[:2]
            # shrink the frame, since non-Qt backend cannot accept window resize
            frame = cv2.resize(
                frame,
                (width/2, height/2),
                interpolation = cv2.INTER_CUBIC
            )

            cv2.imshow('Live Stream', frame)
            # throttle at 100FPS, aka 10ms delay
            cv2.waitKey(10)

        # update the FPS counter
        fps.update()
    except KeyboardInterrupt:
        break

print('Ctrl+C captured, stopping acquisition...')

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

stream.stop()
kairos.stop()
cv2.destroyAllWindows()
