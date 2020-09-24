from multiprocessing import Process

import os

import sys

from PIL import Image

imagename = sys.argv[1]

##########RESIZE IMAGE############ MAY LOSE COORDINATE DATA
basewidth = 1440
img = Image.open(imagename)
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(imagename)
##########RESIZE IMAGE############ MAY LOSE COORDINATE DATA

def loop_yolo():
        command = "export DISPLAY=:0 && ./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights " + imagename + " -i 0 -thresh 0.7"
        #command = "export DISPLAY=:0 && ./darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights " + imagename + " -i 0 -thresh 0.7"
        os.system(command)

def loop_coord():
        command = "python3 GeoFinderWin.py " + imagename
        os.system(command)

if __name__ == '__main__':
    Process(target=loop_yolo).start()
    Process(target=loop_coord).start()
