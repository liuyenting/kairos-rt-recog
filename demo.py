from __future__ import print_function
import argparse
from time import sleep
import cv2
from stream import WebcamVideoStream
from fps import FPS

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--display', action='store_true', default=False,
    help='Whether or not frames should be displayed'
)
args = vars(parser.parse_args())

cv2.namedWindow('Live Stream', cv2.WINDOW_NORMAL)
#TODO window resize is not working
cv2.resizeWindow('Live Stream', 640, 360)

stream = WebcamVideoStream(src=0).start()
fps = FPS().start()

while True:
    try:
        # grab a frame
        frame = stream.read()

        if args['display']:
            # get the size
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

# do a bit of cleanup
cv2.destroyAllWindows()
stream.stop()
