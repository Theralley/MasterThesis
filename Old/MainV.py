from multiprocessing import Process

import os

import sys

from PIL import Image

import moviepy.editor as mp

imagename = sys.argv[1]

#clip = mp.VideoFileClip(imagename)
#clip_resized = clip.resize(height=360) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
#clip_resized.write_videofile(imagename)

def loop_yolo():
        command = "export DISPLAY=:0 && ./darknet detector demo cfg/coco.data yolov4.cfg yolov4.weights " + imagename + " video?dummy=param.mjpg -i 0"
        #command = "export DISPLAY=:0 && ./darknet detector demo cfg/coco.data yolov3-tiny.cfg yolov3-tiny.weights " + imagename + " video?dummy=param.mjpg -i 0"
        os.system(command)

def loop_coord():
        command = "python3 GeoFinderWin.py " + imagename
        os.system(command)

if __name__ == '__main__':
    Process(target=loop_yolo).start()
    #Process(target=loop_coord).start()
