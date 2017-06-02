# import the necessary packages
from __future__ import print_function
from stream import WebcamVideoStream
from fps import FPS
import argparse
import cv2
import signal

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-n", "--num-frames", type=int, default=100,
    help="# of frames to loop over for FPS test"
)
parser.add_argument(
    '-d', '--display', action='store_true',
    help='Whether or not frames should be displayed'
)
args = vars(parser.parse_args())

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")

cv2.namedWindow('Live Stream', cv2.WINDOW_NORMAL)
#TODO window resize is not working
cv2.resizeWindow('Live Stream', 640, 360)

stream = WebcamVideoStream(src=0).start()
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = stream.read()
	#frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if args['display'] > 0:
		cv2.imshow('Live Stream', frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
stream.stop()
