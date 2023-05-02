import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns


data = np.loadtxt(fname=r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation-01.csv", delimiter=',')

# image = plt.imshow(data)
# avg_inflammation = np.mean(data, axis=0)
# avg_plot = plt.plot(avg_inflammation)
# maxplot = plt.plot(np.amax(data, axis=0))
# minplot = plt.plot(np.amin(data, axis=0))
# plt.show()

# plot a figure (i.e. somewhere to plot multiple plots together
fig = plt.figure(figsize=(10.0, 3.0))

# add_subplot takes 3 parameters (total rows, total columns, position
# of plot in matrix)
axes1 = fig.add_subplot(1, 4, 1)
axes2 = fig.add_subplot(1, 4, 2)
axes3 = fig.add_subplot(1, 4, 3)
axes4 = fig.add_subplot(1, 4, 4)

axes1.set_ylabel('Average')
axes1.plot(np.mean(data, axis=0))

axes2.set_ylabel('Maximum')
axes2.plot(np.amax(data, axis=0))

axes3.set_ylabel('Minimum')
axes3.plot(np.amin(data, axis=0))
axes3.set_ylim(0, 6)

axes4.set_ylabel('Standard Deviation')
axes4.plot(np.std(data, axis=0))

fig.tight_layout()

sns.heatmap(data)
plt.show()

plt.savefig('inflammation.png')