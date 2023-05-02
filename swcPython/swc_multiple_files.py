import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# glob searches within a directory for mutliple files,
# * matches zero or more characters
# ? matches any one character

# print(glob.glob(r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation*.csv"))

filenames = sorted(glob.glob(r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation*.csv"))
#filenames = filenames[:3]

# for filename in filenames:
#     print(filename)
#     data = np.loadtxt(fname=filename, delimiter =',')
#
#     fig = plt.figure(figsize=(10,3))
#     axes1 = fig.add_subplot(1, 4, 1)
#     axes2 = fig.add_subplot(1, 4, 2)
#     axes3 = fig.add_subplot(1, 4, 3)
#     axes4 = fig.add_subplot(1, 4, 4)
#
#     axes1.set_ylabel('Average')
#     axes1.plot(np.mean(data, axis=0))
#
#     axes2.set_ylabel('Maximum')
#     axes2.plot(np.amax(data, axis=0))
#
#     axes3.set_ylabel('Minimum')
#     axes3.plot(np.amin(data, axis=0))
#
#     axes4.set_ylabel('Heatmap')
#     sns.heatmap(data, ax=axes4)
#
#     fig.tight_layout()
# plt.show()

# plotting the difference between test 1 and test 2 averages. Note you had to loadtxt
# data1, data2 = np.loadtxt(filenames[0], delimiter=','), np.loadtxt(filenames[1], delimiter=',')
# data_diff = np.mean(data1, axis=0) - np.mean(data2, axis=0)
# plt.plot(data_diff)
# plt.show()

# Use each of the files once to generate a dataset containing values averaged over all patient
composite_data = np.zeros((60,40))
for filename in filenames:
    data=np.loadtxt(fname= filename, delimiter=',')
    composite_data = composite_data + data
# and then divide the composite_data by number of samples
composite_data = composite_data / len(filenames)

fig = plt.figure(figsize = (10,3))
fig.suptitle('Composite Data')

axes1 = fig.add_subplot(1,4,1)
axes2 = fig.add_subplot(1,4,2)
axes3 = fig.add_subplot(1,4,3)
axes4 = fig.add_subplot(1, 4, 4)

axes1.set_ylabel('Average')
axes1.plot(np.mean(composite_data, axis=0))

axes2.set_ylabel('Maximum')
axes2.plot(np.amax(composite_data, axis=0))

axes3.set_ylabel('Minimum')
axes3.plot(np.amin(composite_data, axis=0))

axes4.set_ylabel('Heatmap')
sns.heatmap(composite_data, ax=axes4)

plt.show()