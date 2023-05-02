import numpy
import time



data = numpy.loadtxt(fname=r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation-01.csv", delimiter=',')
print(data)
#
# print(type(data))
# print(data.dtype)
# print(data.shape)
#
# print('first value in data:', data[0, 0])
# print('middle value in data:', data[29, 19])
#
# print(data[0:4, 0:10])
#
# print(numpy.mean(data))
#
# print(time.ctime())
#
# maxval, minval, sdval = numpy.amax(data), numpy.amin(data), numpy.std(data)
#
# # creates array with row 0, all columns, axis 0 = rows, axis 1 = columns
# patient_0 = data[0, :]
# print('maximum inflammation for patient 0:', numpy.amax(patient_0))
#
# print(numpy.mean(data, axis=0).shape)
#
# element = 'oxygen'
# element1= 'carpentry'
# element2 = 'hi'
# print(element[1:4])
# print(element[-3:])
# print(element1[-3:])

A = numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# stack array horizontally
B = numpy.hstack([A, A])
print(A)
print(B)

# diff takes the difference between consecutive values, so will return one less
# element per row
patient3_diff = numpy.diff(data[3, :])
print(patient3_diff)





