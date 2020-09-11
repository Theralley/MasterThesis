from PIL import Image
from PIL.ExifTags import TAGS

from multiprocessing import Process

import os
import time

import sys
from sys import exit

run_once = '0'

degree_sign = u"\N{DEGREE SIGN}"

imagename = "3.jpg"
image = Image.open(imagename)

def loop_yolo():
    while(1):
        command = "./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights " + imagename + " -i 0 -thresh 0.25"
        os.system(command)
        break

def loop_coord():
        time.sleep(10)
        # extract EXIF data
        exifdata = image.getexif()

        # iterating over all EXIF data fields
        for tag_id in exifdata:

            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)

            # Use the tag of the pic
            if(tag_id == 34853):
                print('\nPicName: ', imagename)

                a1 = data[2][0]
                b1 = data[2][1]
                c1 = data[2][2]

                a2 = data[4][0]
                b2 = data[4][1]
                c2 = data[4][2]

                H = data[6]

                dd1 = a1 + (b1/60) + (float(c1)/3600)
                dd2 = a2 + (b2/60) + (float(c2)/3600)

                coord = dd1, dd2

                str(coord)

                print('Coordinates: ' + str(coord))
                print('Height:', H)

                #Picture coord to text
                f= open("coord.txt","a+")
                f.write('PicName: ' + imagename +'\nCoordinates: '+ str(coord) + ' Height: ' + str(H) + '\n \n')
                f.close()


if __name__ == '__main__':
    Process(target=loop_yolo).start()
    Process(target=loop_coord).start()
