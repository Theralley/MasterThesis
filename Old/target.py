# import the necessary packages
import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
# load the video
#camera = cv2.VideoCapture(args["video"])
camera = cv2.VideoCapture(2)

for x in range(0, 0):
    _,frame= camera.read()
# keep looping
while True:
	# grab the current frame and initialize the status text

	(grabbed, frame) = camera.read()
	# check to see if we have reached the end of the
	# video
	if not grabbed:
		break
	# convert the frame to grayscale, blur it, and detect edges
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert it to hsv

	#cv2.imshow("Before", frame)
	frame_c = frame

	b, g, r = cv2.split(frame)
	#print(b, g, r)

	b = r + 50

	frame = cv2.merge((b, g, r))

	#frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

	#cv2.imshow("After", final_hsv)

	gray = frame
    

	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	blurred = cv2.GaussianBlur(gray, (3, 3), 5)
	edged = cv2.Canny(blurred, 100, 400)
	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cv2.imshow("Image2",edged)
	#print(frame.shape[0],frame.shape[1])
	cnts = imutils.grab_contours(cnts)
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
		# ensure that the approximated contour is "roughly" rectangular
		if len(approx) >= 2 and len(approx) <= 100:
			# compute the bounding box of the approximated contour and
			# use the bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			#print(x, y, w, h)
			aspectRatio = w / float(h)
			# compute the solidity of the original contour
			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c)) + 10
			solidity = area * area / float(hullArea)
			# compute whether or not the width and height, solidity, and
			# aspect ratio of the contour falls within appropriate bounds
			keepDims = h/w >= 0.01
			keepSolidity = solidity > 500
			keepAspectRatio = aspectRatio >= 0.6 and aspectRatio <= 2.0
			# ensure that the contour passes all our tests
			if keepDims and keepSolidity and keepAspectRatio:
				# draw an outline around the target and update the status
				# text
				cv2.drawContours(frame_c, [approx], -1, (0, 0, 255), 4)
                # compute the center of the contour region and draw the
				# crosshairs
				#M = cv2.moments(approx)

	# show the frame and record if a key is pressed
	cv2.imshow("Frame", frame_c)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
