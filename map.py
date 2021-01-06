import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

line_count = 0

#Tracking of DJI drone long/lat from csv
df = pd.read_csv("r2.txt")

#Copy TA15
file_TA15 = open("out_TA15.txt","w")
file_TA15.write("x,y,l\n");

#Copy Person
file_person = open("out_person.txt","w")
file_person.write("x,y,l\n");

#Orginal from pynextgen
out = pd.read_csv("out.txt")
file1 = open("out.txt","r")
#Counter
for line in file1:
    if line != "\n":
        line_count += 1
line_count = line_count - 1

#Startpos from drone
startpos = [16.428125, 59.405547]

#angle compared to north, - to left, + to right
angle = -120

#Radius of the Earth
R = 6378.1

#FoorLopp of calcilation to calculate long/lat
for x in range(line_count):
    if(out.label[x] == "TA15"):
        brng2 = math.radians(angle+out.angle[x])

        d = out.l[x]*0.001 #Distance in km

        lat1 = math.radians(startpos[1]) #Current lat from drone point converted to radians
        lon1 = math.radians(startpos[0]) #Current long from drone point converted to radians

        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng2)) #New long

        lon2 = lon1 + math.atan2(math.sin(brng2)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2)) #New lat

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        #print(lat2, lon2) #Test

        file_TA15.write(str(lon2)); file_TA15.write(","); file_TA15.write(str(lat2)); file_TA15.write(","); file_TA15.write(str(d)); file_TA15.write("\n"); #write to file_TA15

file_TA15.close()

for x in range(line_count):
    if(out.label[x] == "person"):
        brng2 = math.radians(angle+out.angle[x])

        d = out.l[x]*0.001 #Distance in km

        #lat2  52.20444 - the lat result I'm hoping for
        #lon2  0.36056 - the long result I'm hoping for.
        lat1 = math.radians(startpos[1]) #Current lat point converted to radians
        lon1 = math.radians(startpos[0]) #Current long point converted to radians

        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng2))

        lon2 = lon1 + math.atan2(math.sin(brng2)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        #print(lat2, lon2)

        file_person.write(str(lon2)); file_person.write(","); file_person.write(str(lat2)); file_person.write(","); file_person.write(str(d)); file_person.write("\n");

file_person.close()

out_TA15 = pd.read_csv("out_TA15.txt")
out_person = pd.read_csv("out_person.txt")

ruh_m = plt.imread('map.png')

img_cropped = ruh_m[77:141, 57:121, :]

fig, ax = plt.subplots(figsize = (12,9))

ax.scatter((out_TA15.x), (out_TA15.y), zorder=2, alpha= 1, c='y', s=300, marker='s')
ax.scatter((out_person.x), (out_person.y), zorder=2, alpha= 1, c='g', s=300, marker='s')
ax.scatter(startpos[0], startpos[1], zorder=2, alpha= 1, c='r', s=12)

ax.set_title('Plotting Data on Volvo Eskilstuna, Green = Person, Yellow = TA15, Red = Position of Drone')

#Sets limits
xmin = 16.42372
xmax = 16.43711
ymin = 59.40307
ymax = 59.40811

xmin1 = df.longitude.min()*0.999995
xmax1 = df.longitude.max()*1.000005
ymin1 = df.latitude.min()*0.999995
ymax1 = df.latitude.max()*1.000005

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

BBox = (xmin, xmax, ymin, ymax)

ax.set_axisbelow(True)
ax.minorticks_on()
ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

#Plots
ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
rectangle = patches.Rectangle((xmin1, ymin1), xmax1-xmin1, ymax1-ymin1, fill=False)

ax.add_patch(rectangle)
plt.plot(xmin,xmax)
plt.show()
