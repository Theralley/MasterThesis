import cv2
import numpy as np
import time
import sys
import imutils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

imagename = sys.argv[1]
yoloV = sys.argv[2]
tt = sys.argv[3]

a = 1

xo = 0
yo = 0
diff = 2

yxdiff = 1
yydiff = 1

t = 0

line_thickness = 2

# keep looping
#Load YOLO
if(yoloV == "v4"):
    net = cv2.dnn.readNet("yolov4.weights","yolov4.cfg") # Original yolov3

if(yoloV == "v3-tiny"):
    net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") # Original yolov3

if(yoloV != "v3-tiny" and yoloV != "v4"):
    print("Enter value after video name for Weight: v4, v3-tiny")
#net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
classes = []
with open("coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

#print(classes)

im = mpimg.imread("ResultTemp.png")
cv2.imwrite("ResultDot.png",im)
im = mpimg.imread("ResultDot.png")

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0,255,size=(len(classes),3))

#loading image
font = cv2.FONT_HERSHEY_PLAIN
frame_id = 0
cap = cv2.VideoCapture(imagename)

#FRAM TO START ON#
for x in range(0, int(tt)):
    _,frame= cap.read()

while True:
    (grabbed, frame) = cap.read()

    #JUMPOVER PICTURES#
    for x in range(0, 0):
        _,frame= cap.read()

    if not grabbed:
        break
        print("ERROR WHILE GRAB")

    ##CHANGE COLOR SPECTRUM
    b, g, r = cv2.split(frame)
    frame = cv2.merge((b, g, r))

    #detecting objects
    blob = cv2.dnn.blobFromImage(frame,0.00392,(416,416),(0,0,0),True,crop=False) #reduce 416 to 320

    net.setInput(blob)
    outs = net.forward(outputlayers)
    #print(outs[1])
    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]

    height,width,channels = frame.shape
    #print(frame.shape[1])

    #########EDGE FIXES############
    # convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 5)
    edged = cv2.Canny(blurred, 100, 400)
    #find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("Edged",edged)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    	# ensure that the approximated contour is "roughly" rectangular
    	if len(approx) >= 3 and len(approx) <= 500:
    		# compute the bounding box of the approximated contour and
    		# use the bounding box to compute the aspect ratio
    		(x, y, w, h) = cv2.boundingRect(approx)
    		aspectRatio = w / float(h)
    		# compute the solidity of the original contour
    		area = cv2.contourArea(c)
    		hullArea = cv2.contourArea(cv2.convexHull(c))
    		solidity = area / float(hullArea)
    		# compute whether or not the width and height, solidity, and
    		# aspect ratio of the contour falls within appropriate bounds
    		keepDims = w > 0 and h > 35
    		keepSolidity = solidity > 0.9
    		keepAspectRatio = aspectRatio >= 0.4 and aspectRatio <= 2.0
    		# ensure that the contour passes all our tests
    		if keepDims and keepSolidity and keepAspectRatio:

                 if(y == 0):
                     y = 1
                 if(x == 0):
                     x = 1

                 xdiff = (xo/x)
                 ydiff = (yo/y)

                 if xdiff < 0.5 or xdiff > 1.3 or ydiff < 0.5 or ydiff > 1.3:
                     cv2.putText(frame," UNDEFINED OBJECT; BE CAREFUL ", (x,y+200),font,1,(255,0,0),2)
                     #print("ERROR")
                 else:
                     cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                     #print("Contour XY:     ", x,y , " | Difference X : ", (xdiff), " | Difference Y : ", (ydiff))
                     #print(approx[5][0][0])
                     cv2.putText(frame,"TA15", (x,y+200),font,1,(255,0,0),2)
                     cv2.line(frame, (approx[0][0][0], approx[0][0][1]), (approx[3][0][0], approx[3][0][1]), (0, 255, 0), thickness=line_thickness)

                     #im = np.zeros((frame.shape[0],frame.shape[1],3),np.uint8)
                     im = cv2.circle(im, (approx[0][0][0], approx[0][0][1]), radius=5, color=(0, 0, 255), thickness=-1)
                     t = t + 1

                     if(t == 100):
                        cv2.imwrite("ResultDot.png",im)
                        t = 0

                 xo = x
                 yo = y

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

            #print('Before: '+ label)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,0,0),2)
            #print(label+" "+str(round(confidence,2)))

            if(label == "person" or label == "TA15" or label == "truck" or label == "car"or label == "motorbike"):
                print("Yolo XY:        ", x,y," | Confidence: ", str(round(confidence,2)), " | Differs: ", yydiff, yxdiff)
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(255,0,0),2)
                #cv2.imwrite('PythonResult/%d.jpg' % a , frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                #a = a + 1
            else:
                cv2.circle(frame,(center_x,center_y),10,(0,255,0),2)
                cv2.putText(frame," UNDEFINED OBJECT; BE CAREFUL ",(x,y+30),font,1,(255,0,0),2)
                #print('After: '+ label)

    cv2.imshow("Image",frame)
    key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame

    if key == 27: #esc key stops the process
        cv2.imwrite("ResultDot.png",im)
        break;

cap.release()
cv2.destroyAllWindows()
