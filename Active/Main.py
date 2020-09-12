from PIL import Image
from PIL.ExifTags import TAGS

from multiprocessing import Process

import os
import time

import sys
from sys import exit

imagename = "3.jpg"

def loop_yolo():
        command = "export DISPLAY=:0 && ./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights " + imagename + " -i 0 -thresh 0.25"
        os.system(command)

def loop_coord():
        command = "python3 GeoFinderWin.py " + imagename
        os.system(command)

if __name__ == '__main__':
    Process(target=loop_yolo).start()
    Process(target=loop_coord).start()
