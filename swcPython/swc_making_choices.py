import numpy as np

data = np.loadtxt(fname=r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation-03.csv", delimiter=',')
max_inflammation_0 = np.amax(data, axis=0)[0]
max_inflammation_20 = np.amax(data, axis=0)[20]

if max_inflammation_0 == 0 and max_inflammation_20 == 20:
    print('This shit looks wack!')
elif np.sum(np.amin(data, axis=0)) == 0:
    print('Minima are all zero!')
else:
    print('Seems alright!')

# a= 120
# b=100
#
# if a<=1.1*b and a>=0.9*b:
#     print('a is within 10% of b')


# sorting filenames based on what they start with
filenames = ['inflammation-01.csv',
         'myscript.py',
         'inflammation-02.csv',
         'small-01.csv',
         'small-02.csv']

large_files=[]
small_files = []
other_files = []

for files in filenames:
    if files.startswith('inflammation'):
        large_files.append(files)
    elif files.startswith('small'):
        small_files.append(files)
    else:
        other_files.append(files)
print(large_files, small_files, other_files)

# snippet that checks sentence for vowels
vowels = 'aeiouAEIOU'
sentence = 'Hi Im Mike Tyson and watch me on cumcast cablevision'
count=0
for char in sentence:
    if char in vowels:
        count +=1
print('The count is:', count)