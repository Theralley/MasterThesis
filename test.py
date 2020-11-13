from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

# Two example plots
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)

spacing = 0.5 # This can be your user specified spacing.
minorLocator = MultipleLocator(spacing)
ax1.plot(9 * np.random.rand(10))
# Set minor tick locations.
ax1.yaxis.set_minor_locator(minorLocator)
ax1.xaxis.set_minor_locator(minorLocator)
# Set grid to use minor tick locations.
ax1.grid(which = 'minor')

plt.show()
