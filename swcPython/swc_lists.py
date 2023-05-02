# lists are inbuilt

# lists are built inside  square brackets separated by commas
odds = [1, 3, 5, 7]
print('The odds are:', odds)

# access elements of a list using indexing (note that first is 0)
print('first element', odds[0])

# elements in a list can bee changed, parts in a string cannot
names = ['Curie', 'Darwing', 'Turing']
print('wrong names are', names)

# change Darwing
names[1]= 'Darwin'
print('Correct names are', names)

# mutable can be changed without assiging totally new values,
# immutable cannot. Lists and arrays are mutable
hot_salsa = ['Peppers', 'Onion', 'Cheese']

# creates list that is copy of original but can be modified independently
mild_salsa = list(hot_salsa)
mild_salsa[0] = 'Hot as fuck peppers'
print(mild_salsa)
print(hot_salsa)

# Lists can be nested in other lists
supermarket = [['pepper', 'cheese', 'jam'],
               ['tomato', 'chilli'],
                ['sauce', 'sauce', 'choc']]
print(supermarket[0][1])

string_for_slicing = 'Observation date: 02-Feb-2013'
print(string_for_slicing[-4:])
list_for_slicing = [['fluorine', 'F'],
                    ['chlorine', 'Cl'],
                    ['bromine', 'Br'],
                    ['iodine', 'I'],
                    ['astatine', 'At']]

print(list_for_slicing[-4:])

# adding another value to the slice will act as a step size
beatles = "In an octopus's garden in the shade"
print(beatles[0:35:2])

# + concatenates strings and * replicates and concatenates x number of times
evens = [2, 4, 6, 8]
print(evens + evens)
print(evens * 3)
