odds = [1, 3, 5, 7]

# for variable in collection:
# loop variable name e.g. num doesn't matter
for num in odds:
    print(num)

length = 0
names = ['Curie', 'Darwin', 'Turing']
for value in names:
    length = length + 1
print('There are', length, 'names in the list.')

# len finds the length of an object (list, array)
print(len(names))

ranges = [list(range(5)),
        list(range(4,8)),
       list(range(4,8,2))
          ]

for value in ranges:
    print(value)

# practicing a for loop to sum numbers
nums = [124, 402, 36]
total = 0
for val in nums:
    total = total + val
    print('Running total:', total)
print('Final total is:', total)

# enumerate function takes a list and produces a new list with that index and value

coefs = [2, 4, 3]
x = 5
y = 0
for idx, coefs in enumerate(coefs):
    y = y + coefs * x**idx
    print(y)

