import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

df = pd.read_csv("r2.txt")
out = pd.read_csv("out.txt")

#Video 6.mp4
startpos = [16.428125, 59.405547]
#angle compared to north
angle = 65

#df.head()

ruh_m = plt.imread('map.png')
print(ruh_m.shape)

img_cropped = ruh_m[77:141, 57:121, :]
# confirm cropped image shape
print(img_cropped.shape)

fig, ax = plt.subplots(figsize = (12,9))

ax.scatter(df.longitude, df.latitude, zorder=2, alpha= 0.1, c='g', s=12)
ax.scatter(startpos[0], startpos[1], zorder=2, alpha= 1, c='r', s=12)
ax.scatter(out.x, out.y, zorder=2, alpha= 0.1, c='r', s=12)

ax.set_title('Plotting Spatial Data on Riyadh Map')

#print(df.longitude)
#print(df.latitude)

print(df.longitude.min(), df.longitude.max(), df.latitude.min(), df.latitude.max())

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
