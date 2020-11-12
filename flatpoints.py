import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("out.txt")

#df.head()

ruh_m = plt.imread('ResultTemp.png')

fig, ax = plt.subplots(figsize = (12,9))

#Närstående 20^2+40^2=48^2, 20*2.4 = 48, -400 (offset)
ax.scatter(df.x, (df.y*2.4)-400, zorder=1, alpha= 0.1, c='r', s=9)

ax.set_title('Plotting points as Angled Camera')

print(df.x[1])

xmin = 0
xmax = 1280
ymin = 720
ymax = 0

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

BBox = (xmin, xmax, ymin, ymax)

ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
plt.show()