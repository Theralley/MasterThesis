import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

line_count = 0

df = pd.read_csv("r2.txt")
out = pd.read_csv("out.txt")
file = open("out_c.txt","w")

file.write("x,y,l,offset\n");

file1 = open("out.txt","r")

for line in file1:
    if line != "\n":
        line_count += 1

line_count = line_count - 1

startpos = [16.428125, 59.405547]
#angle compared to north, - to left, + to right
angle = -30

R = 6378.1 #Radius of the Earth
brng = math.radians(angle) #Bearing is 90 degrees converted to radians.

for x in range(line_count):

    d = out.l[x]*0.001 #Distance in km

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.
    lat1 = math.radians(startpos[1]) #Current lat point converted to radians
    lon1 = math.radians(startpos[0]) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    file.write(str(lon2)); file.write(","); file.write(str(lat2));file.write(","); file.write(str(d)); file.write("\n");

file.close()

out = pd.read_csv("out_c.txt")
#print(out.x[1])
#df.head()

ruh_m = plt.imread('map.png')
#print(ruh_m.shape)

img_cropped = ruh_m[77:141, 57:121, :]
# confirm cropped image shape
#print(img_cropped.shape)

fig, ax = plt.subplots(figsize = (12,9))

#ax.scatter(df.longitude, df.latitude, zorder=2, alpha= 0.1, c='g', s=12)
#ax.scatter(startpos2[0], startpos2[1], zorder=2, alpha= 1, c='r', s=100, marker='s')
ax.scatter((out.x-0.0002), (out.y-0.0001), zorder=2, alpha= 1, c='r', s=300, marker='s')
ax.scatter(startpos[0], startpos[1], zorder=2, alpha= 1, c='b', s=12)

ax.set_title('Plotting Spatial Data on Riyadh Map')

#print(df.longitude)
#print(df.latitude)

#print(df.longitude.min(), df.longitude.max(), df.latitude.min(), df.latitude.max())

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

#ax.xaxis.zoom(1)
#ax.yaxis.zoom(1)

ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')

rectangle = patches.Rectangle((xmin1, ymin1), xmax1-xmin1, ymax1-ymin1, fill=False)
ax.add_patch(rectangle)

plt.plot(xmin,xmax)



plt.show()
