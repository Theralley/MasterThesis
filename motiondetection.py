#Verison: 0.1.7
#Author: Rhn15001, Rasmus Hamren
#Applying UAVs to Support the Safety in Autonomous Operated Open Surface Mines
from imutils.video import VideoStream
import argparse
import imutils
import cv2
import matplotlib.image as mpimg
import statistics
import sys
import math

line = 0

font = cv2.FONT_HERSHEY_PLAIN

i = 0
x = 1; y = 1; xo = 0; yo = 0; ho = 0; wo = 0; xv = 0; yv = 0; ao = 0; w = 0
h = 0

loop_stopper = loop_stopper2 = 0

a = 0
r = 0; oldC = 0

line_thickness = 2

radius = 0
radiusO = 0
circleO = 0

square = 0

heightD = 20
camangle = 20

md = (int(heightD)/(math.sin(math.radians(90)-math.radians(int(camangle)))))
md = int(md)

file = open("outMotion.txt","w")
file.write("label,x,y,l,angle,offset\n");

im = mpimg.imread("ResultTemp.png")
cv2.imwrite("ResultDot.png",im)
im = mpimg.imread("ResultDot.png")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# If video input is none, open webcam (only works in real Ubuntu eviroment)
if args.get("video", None) is None:
	cap = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, read video input
else:
	cap = cv2.VideoCapture(args["video"])

# initialize the first frame
firstFrame = None

# loop over the frames of the video
while True:

	# grab the current frame and initialize
	frame = cap.read()
	frame = frame if args.get("video", None) is None else frame[1]

	# if a frame is none, end of video
	if frame is None:
		break

	if(frame.shape[1] > 0 and loop_stopper == 0):
	    pl = po = (frame.shape[1] * 0.021875)
	    loop_stopper = 1

	# resize, convert it to grayscale, and blur it
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (3, 3), 5)
	gray = cv2.Canny(gray, 200, 200)

	# save frame buffer
	if firstFrame is None:
		firstFrame = gray
		continue

	# absolute difference
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# create threshold and find contours
	thresh = cv2.dilate(thresh, None, iterations=1)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# saving buffer in frames, can be changed but can not be used on UAV if other
	for c in cnts:
		if i == 1:
			firstFrame = gray
			i = 0
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 200:
			continue

		# compute box

		(x, y, w, h) = cv2.boundingRect(c)

		w = wo*0.7+w*0.3
		h = ho*0.7+h*0.3

		square = cv2.rectangle(frame, (int(x), int(y)), (int(x) + int(w),
		int(y) + int(h)), (0, 255, 0), 2)

		xv = x - xo
		yv = y - yo

		#creating radius and safety circles, but since no real size is being
		#introduced this is will be for future work
		radius=int(80*(w/h))
		radius = radiusO*0.95+radius*0.05
		radiusO = radius

		circle = cv2.circle(frame, (int(x+w/2), int(y+h/2)), int(radius),
		color=(0, 0, 255), thickness=1)

		#Buffer
		circleO = circle
		if(a == 15):
			xo = x; yo = y; wo = w; ho = h
			a = 0
		ao = a

		#Circle print
		im = cv2.circle(im, (int(x), int(y)),
		radius=4, color=(0, 0, 255), thickness=-1)

		angle2 = math.atan2(frame.shape[1]/2 - int(y+(h/2)),
		int(x+(w/2)) - frame.shape[1]/2) * 180.0 / math.pi

		angle2 = 90 - angle2

		#Prints xy coorinates on the frame
		#print(int(x), int(y))
		p1 = [frame.shape[1]/2, frame.shape[0]]
		p2 = [x, y]
		distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

		ans = md/(frame.shape[0]/2)
		distance = ans * distance

		pl = h
		pl = pl*0.6+po*0.4
		po = pl
		lp = 2.3/pl

		c2 = math.sqrt((((int(frame.shape[1]/2)-x) * (lp))*
		((int(frame.shape[1]/2)-x) * (lp)) + (md*md)))
		c3 = (c2 + distance)/2

		file.write("motion"); file.write(",");
		file.write(str(int(x+(w/2)))); file.write(",");
		file.write(str(int(y+(h/2)))); file.write(","); file.write(str(c3));
		file.write(","); file.write(str(angle2)); file.write(",");
		file.write("0"); file.write("\n");

	square = cv2.rectangle(frame, (int(x), int(y)),
	(int(x) + int(w), int(y) + int(h)), (0, 255, 0), 2)

	circle = cv2.circle(frame, (int(x+w/2), int(y+h/2)),
	int(radius), color=(0, 0, 255), thickness=1)

	cv2.imshow("Motion detection", frame)
	a = int(a) + 1
	i = i + 1

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

cap.stop() if args.get("video", None) is None else cap.release()
cv2.destroyAllWindows()
