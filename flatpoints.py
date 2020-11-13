import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

line_count = 0

df = pd.read_csv("out.txt")
file1 = open("out.txt","r")

file = open("flip.txt","w")
file.write("x,y\n");
i = 0

for line in file1:
    if line != "\n":
        line_count += 1

line_count = line_count - 1

#angle compared to north
angle = -48

xmin = 0
xmax = 1280
ymin = 900
ymax = 0

qx = 0; qy = 0;

origin=(xmax/2,ymin/2)

#df.head()

ruh_m = plt.imread('ResultTemp.png')

fig, ax = plt.subplots(figsize = (12,9))

#Närstående 20^2+40^2=48^2, 20*2.4 = 48, -400 (offset)
ax.scatter(df.x, (df.y), zorder=1, alpha= 0.1, c='g', s=9)
ax.scatter(df.x, (df.y*2.4)-400, zorder=1, alpha= 0.1, c='r', s=9)

for x in range(line_count):
    file.write(str(df.x[x])); file.write(","); file.write(str((df.y[x]*2.4)-400)); file.write("\n");


for x in range(line_count):
    point = df.x[x], (df.y[x]*2.4)-400

    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
    qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)

    df.x[x] = qx
    df.y[x] = qy
ax.scatter(df.x, (df.y), zorder=1, alpha= 0.1, c='b', s=9)

ax.set_title('Plotting points as Angled Camera')

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

BBox = (xmin, xmax, ymin, ymax)

ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
plt.show()
