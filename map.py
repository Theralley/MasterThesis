import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("r3.txt")

#df.head()

ruh_m = plt.imread('map.png')

fig, ax = plt.subplots(figsize = (12,9))

ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.1, c='r', s=9)

ax.set_title('Plotting Spatial Data on Riyadh Map')

print(df.longitude)
print(df.latitude)

xmin = 16.42372
xmax = 16.43711
ymin = 59.40307
ymax = 59.40811

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

BBox = (xmin, xmax, ymin, ymax)

ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
plt.show()
