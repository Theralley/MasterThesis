import cv2
import numpy as np
import time
import sys
import math
from math import sin
import imutils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.transform import (hough_line, hough_line_peaks)

imagename = sys.argv[1]
yoloV = sys.argv[2]
tt = sys.argv[3]
heightD = sys.argv[4]
camangle = sys.argv[5]

file = open("out.txt","w")
file.write("label,x,y,l,angle,offset\n");

md = (int(heightD)/(math.sin(math.radians(90)-math.radians(int(camangle)))))
md = int(md)

#Variables
c2 = 0
a = 1
xo = 0; xsave = 0; xsaveV = 0
yo = 0; ysave = 0; wsave = 0; ysaveV = 0; wsaveV = 0
diff = 2
yxdiff = 1
yydiff = 1
t = 0
line_thickness = 2
Multiplier = 0.5
OldCentrumX = 0
OldCentrumY = 0
add = 0
bertil = bertil2 = 0
run_between = 0

#Load YOLO
if(yoloV == "v4"):
    net = cv2.dnn.readNet("yolov4.weights","yolov4.cfg") # Original yolov3

if(yoloV == "v3-tiny"):
    net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") # Original yolov3

if(yoloV == "v4-tiny"):
    net = cv2.dnn.readNet("yolov4-tiny.weights","yolov4-tiny.cfg") # Original yolov3

if(yoloV != "v3-tiny" and yoloV != "v4" and yoloV != "v4-tiny"):
    print("Enter value after video name for Weight: v4, v3-tiny")

classes = []

with open("coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

#Load CV
im = mpimg.imread("ResultTemp.png")
cv2.imwrite("ResultDot.png",im)
im = mpimg.imread("ResultDot.png")

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0,255,size=(len(classes),3))

#loading image
if(imagename == '0'):
    imagename = 0

font = cv2.FONT_HERSHEY_PLAIN
frame_id = 0
cap = cv2.VideoCapture(imagename)

#FRAME TO START ON
for x in range(0, int(tt)):
    _,frame= cap.read()

while True:
    (grabbed, frame) = cap.read()

#JUMPOVER PICTURES#
    if(yoloV == "v4-tiny" or yoloV == "v3-tiny"):
        for x in range(0, 5):
            _,frame= cap.read()

    if not (yoloV == "v4-tiny" or yoloV == "v3-tiny"):
        for x in range(0, 10):
            _,frame= cap.read()

#Flip if want to

    time.sleep(0.05)

    if not grabbed:
        break
        print("ERROR WHILE GRAB")

    #########Change brightness in frame############
    if(run_between <= 1):
        frame = cv2.add(frame,np.array([0.0]))
        run_between = run_between + 1
    elif(run_between == 2):
        frame = cv2.add(frame,np.array([-40.0]))
        run_between = 0

    ##CHANGE COLOR SPECTRUM
    b, g, r = cv2.split(frame)
    frame = cv2.merge((b, g, r))

    #detecting objects
    blob = cv2.dnn.blobFromImage(frame,0.00392,(416,416),(0,0,0),True,crop=False) #reduce 416 to 320
    net.setInput(blob)
    outs = net.forward(outputlayers)

    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]

    height,width,channels = frame.shape

    if(frame.shape[1] > 0 and bertil == 0):
        pl = po = (frame.shape[1] * 0.021875)
        bertil = 1

    #########EDGE FIXES############
    # convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame
    blurred = cv2.GaussianBlur(gray, (3, 3), 5)
    edged = cv2.Canny(blurred, 200, 500)

    #find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                #onject detected
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)

                boxes.append([x,y,w,h]) #put all rectangle areas
                confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                class_ids.append(class_id) #name of the object tha was detected

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]

            if(yoloV == "v4" or yoloV == "v3"):
                acc = 0.70

            if not (yoloV == "v4" or yoloV == "v3"):
                acc = 0.40

            if(round(confidence,2) >= acc):
                if(label == "person"):

                    p1 = [frame.shape[1]/2, frame.shape[0]]
                    p2 = [x, y]
                    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

                    ans = md/(frame.shape[0]/2)
                    distance = ans * distance

                    pl = h
                    pl = pl*0.6+po*0.4
                    po = pl
                    lp = 2.3/pl

                    cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                    cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,0,0),2)

                    c2 = math.sqrt((((int(frame.shape[1]/2)-x) * (lp))*((int(frame.shape[1]/2)-x) * (lp)) + (md*md)))
                    c3 = (c2 + distance)/2

                    #Buffer
                    xsave = int(x+(w/2))
                    ysave = int(y+(h/2))
                    wsave = w

                    im = cv2.circle(im, (xsaveV,ysaveV), radius=5, color=(0, 0, 255), thickness=-1)
                    cv2.imwrite("ResultDot.png",im)
                    if(t == 100):
                        cv2.imwrite("ResultDot.png",im)
                        t = 0

                    #Angle from offset calculation (line to offset point, line to object == angle in degree)
                    angle2 = math.atan2(frame.shape[1]/2 - int(y+(h/2)), int(x+(w/2)) - frame.shape[1]/2) * 180.0 / math.pi;
                    angle2 = 90 - angle2

                    file.write(str(label)); file.write(","); file.write(str(int(x+(w/2)))); file.write(","); file.write(str(int(y+(h/2)))); file.write(","); file.write(str(c3)); file.write(","); file.write(str(angle2)); file.write(","); file.write(str(md)); file.write("\n");
                    t = t + 1

                elif(label == "TA15" or label == "truck" or label == "motorbike" or label == "skateboard" or label == "car"):
                    if(label == "motorbike" or label == "skateboard"):
                        label = "TA15"

                    p1 = [frame.shape[1]/2, frame.shape[0]]
                    p2 = [x, y]
                    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

                    ans = md/(frame.shape[0]/2)
                    distance = ans * distance

                    pl = h
                    pl = pl*0.6+po*0.4
                    po = pl
                    lp = 2.3/pl

                    cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                    cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,0,0),2)

                    c2 = math.sqrt((((int(frame.shape[1]/2)-x) * (lp))*((int(frame.shape[1]/2)-x) * (lp)) + (md*md)))
                    c3 = (c2 + distance)/2

                    #Buffer
                    xsaveV = int(x+(w/2))
                    ysaveV = int(y+(h/2))
                    wsaveV = w

                    im = cv2.circle(im, (xsaveV,ysaveV), radius=5, color=(0, 0, 255), thickness=-1)
                    cv2.imwrite("ResultDot.png",im)
                    if(t == 100):
                        cv2.imwrite("ResultDot.png",im)
                        t = 0

                    angle2 = math.atan2(frame.shape[1]/2 - int(y+(h/2)), int(x+(w/2)) - frame.shape[1]/2) * 180.0 / math.pi;
                    angle2 = 90 - angle2

                    file.write(str(label)); file.write(","); file.write(str(int(x+(w/2)))); file.write(","); file.write(str(int(y+(h/2)))); file.write(","); file.write(str(c3)); file.write(","); file.write(str(angle2)); file.write(","); file.write(str(md)); file.write("\n");
                    t = t + 1

                if not (label == "TA15" or label == "truck" or label == "car" or label == "motorbike" or label == "skateboard" or label == "person"):
                    cv2.circle(frame,(center_x,center_y),10,(0,255,0),2)
                    print(label)
                    cv2.putText(frame," UNDEFINED OBJECT; BE CAREFUL ",(x,y+30),font,1,(255,0,0),2)
    for c in cnts:
    	add = add + 1

        # approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.01 * peri, True)

    	# ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 3 and len(approx) <= 500:

            # compute the bounding box of the approximated contour and use the bounding box to compute the aspect ratio
    		(x, y, w, h) = cv2.boundingRect(approx)
    		aspectRatio = w / float(h)

    		# compute the solidity of the original contour
    		area = cv2.contourArea(c)
    		hullArea = cv2.contourArea(cv2.convexHull(c))
    		solidity = area / float(hullArea)

            # compute whether or not the width and height, solidity, and aspect ratio of the contour falls within appropriate bounds
    		keepDims = w > 0 and h > 35
    		keepSolidity = solidity > 0.9
    		keepAspectRatio = aspectRatio >= 0.4 and aspectRatio <= 2.0

    		if keepDims and keepSolidity and keepAspectRatio:

                 if(y == 0):
                     y = 1
                 if(x == 0):
                     x = 1

                 xdiff = (xo/x)
                 ydiff = (yo/y)

                 if xdiff < 0.5 or xdiff > 1.3 or ydiff < 0.5 or ydiff > 1.3:
                     cv2.putText(frame," UNDEFINED OBJECT; BE CAREFUL ", (x,y+200),font,1,(255,0,0),2)

                 else:
                     cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
                     x1 = approx[0][0][0]; y1 = approx[0][0][1]; x2 = approx[3][0][0]; y2 = approx[3][0][1]
                     cv2.putText(frame,"TA15", (x,y+200),font,1,(255,0,0),2)
                     x3 = x2 - x1; y3 = y2 - y1
                     x4 = x1 - x2; y4 = y1 - y2

                     CentrumX = approx[0][0][0]-50; CentrumY = approx[0][0][1]+50

                     #Lines for edge detection
                     cv2.line(frame, (x1, y1), ((x1 - x3*2)+100, (y1 - y3*2)+100), (0, 100, 255), thickness=line_thickness)
                     cv2.line(frame, (x1, y1), ((x1 - x3*3), (y1 - y3*3)), (0, 0, 255), thickness=line_thickness)
                     cv2.line(frame, (x1, y1), ((x1 - x3*2)-100, (y1 - y3*2)-100), (0, 100, 255), thickness=line_thickness)
                     cv2.line(frame, (x2, y2), ((x2 - x4*2)-100, (y2 - y4*2)-100), (0, 0, 255), thickness=line_thickness)
                     cv2.line(frame, (x2, y2), ((x2 - x4*3), (y2 - y4*3)), (0, 0, 255), thickness=line_thickness)
                     cv2.line(frame, (x2, y2), ((x2 - x4*2)+100, (y2 - y4*2)+100), (0, 0, 255), thickness=line_thickness)

                     layedCir = cv2.circle(frame, (CentrumX, CentrumY), radius=200, color=(0, 0, 255), thickness=1)

                     CentrumX = ((((Multiplier*CentrumX)) + ((1 - Multiplier)*OldCentrumX)))
                     CentrumY = ((((Multiplier*CentrumY)) + ((1 - Multiplier)*OldCentrumY)))

                     OldCentrumX = CentrumX; OldCentrumY = CentrumY
                 xo = x
                 yo = y

    #camangle compared to north

    cv2.circle(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)),2,(0,255,0),thickness=-1)

    #Circle Buffer For Safety Distance
    if (wsave < 150 and wsave != 0):
        cv2.circle(frame, (int(xsave), int(ysave)), radius=100+wsave, color=(0, 0, 255), thickness=1)
    wsave = wsave * 1.08
    wsave = int(wsave)

    if (wsaveV < 150 and wsaveV != 0):
        cv2.circle(frame, (int(xsaveV), int(ysaveV)), radius=100+wsaveV, color=(0, 0, 255), thickness=1)
    wsaveV = wsaveV * 1.08
    wsaveV = int(wsaveV)

    cv2.imshow("Image",frame)

    key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame

    if key == 27: #esc key stops the process
        cv2.imwrite("ResultDot.png",im)
        break;

cap.release()
cv2.destroyAllWindows()
