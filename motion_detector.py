# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import cv2
import matplotlib.image as mpimg
import statistics
import sys

line = 0

font = cv2.FONT_HERSHEY_PLAIN

i = 0
x = 1; y = 1; xo = 0; yo = 0; ho = 0; wo = 0; xv = 0; yv = 0; ao = 0; w = 0; h = 0;

a = 0
r = 0; oldC = 0

line_thickness = 2

radius = 0
radiusO = 0
circleO = 0

square = 0

file = open("out.txt","w")
file.write("x,y\n");

im = mpimg.imread("ResultTemp.png")
cv2.imwrite("ResultDot.png",im)
im = mpimg.imread("ResultDot.png")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	cap = VideoStream(src=0).start()
	time.sleep(2.0)
# otherwise, we are reading from a video file
else:
	cap = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = cap.read()
	frame = frame if args.get("video", None) is None else frame[1]
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break
	# resize the frame, convert it to grayscale, and blur it
	motion_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	motion_grey = cv2.GaussianBlur(motion_grey, (3, 3), 5)
	motion_grey = cv2.Canny(motion_grey, 200, 200)
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = motion_grey
		continue
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, motion_grey)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=1)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# loop over the contours
	for c in cnts:
		if i == 1:
			firstFrame = motion_grey
			i = 0
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 180:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)

		medianX = [x, xo]
		medianX = statistics.median(medianX)

		medianY = [y, yo]
		medianY = statistics.median(medianY)

		#print('MedianX: ', medianX , 'A: ', a)
		#print('MedianY: ', medianY)

		(x, y, w, h) = cv2.boundingRect(c)

		w = wo*0.7+w*0.3
		h = ho*0.7+h*0.3

		#square = cv2.rectangle(frame, (int(x), int(y)), (int(x) + int(w), int(y) + int(h)), (0, 255, 0), 2)
		#print(x, y, xo, yo)
		xv = x - xo
		yv = y - yo

		#print(xv, yv)

		#xv = x - xo
		#yv = yv - yo

		#FILTERING
		radius=int(80*(w/h))
		radius = radiusO*0.95+radius*0.05
		radiusO = radius

		circle = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(radius), color=(200, 0, 200), thickness=1)

		#cv2.putText(frame, str(a),(x,y+30),font,1,(255,0,0),2)
		#cv2.circle(frame, (x, y), radius=4, color=(0, 0, 255), thickness=1)
		#cv2.circle(frame, (xo, yo), radius=4, color=(255, 0, 0), thickness=-1)
		#line = cv2.line(frame, ((x), (y)), (xo, yo), (255, 0, 0), thickness=line_thickness)
		#cv2.line(frame, (x, y), ((x + (x-xo)+30), (y - (yo - y))+30), (255, 0, 0), thickness=line_thickness)
		if(a == 15):
			xo = x; yo = y; wo = w; ho = h
			a = 0
		#print('New: ',x, y, '|', w, h)
		#print('Old: ',xo, yo, '|', wo, ho)
		medianA = [x, xo]
		medianA = statistics.median(medianA)
		#print('MedianA: ', medianA)

		im = cv2.circle(im, (int(x), int(y)), radius=4, color=(0, 0, 255), thickness=-1)
		#print(x, xo)
		ao = a
		#cv2.putText(im, str(a),(x,y),font,1,(255,0,0),2)
		cv2.imwrite("ResultDot.png",im)

		print(int(x), int(y))

		file.write(str(x)); file.write(","); file.write(str(y)); file.write("\n");

	#square = cv2.rectangle(frame, (int(x), int(y)), (int(x) + int(w), int(y) + int(h)), (0, 255, 0), 2)
	#circle = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(radius), color=(0, 0, 255), thickness=1)
	cv2.imshow("Security Feed", frame)
	a = int(a) + 1
	i = i + 1

	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
cap.stop() if args.get("video", None) is None else cap.release()
cv2.destroyAllWindows()
