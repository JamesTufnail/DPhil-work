# local variables are only definied within functions and cease to exist
# outside the function. Global variables exist everywhere
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def fahr_to_celsius(temp):
    return ((temp - 32)) * (5 / 9)


def celsius_to_kelvin(temp_c):
    return temp_c + 273.15


def fahr_to_kelvin(temp_f):
    temp_c = fahr_to_celsius(temp_f)
    temp_k = celsius_to_kelvin(temp_c)
    return temp_k


def visualise(filename):
    data = np.loadtxt(fname=filename, delimiter=',')

    fig = plt.figure(figsize=(10, 3))
    fig.suptitle('{}'.format(filename))

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

    axes4.set_ylabel('Heatmap')
    sns.heatmap(data, ax=axes4)

    fig.tight_layout()
    plt.show()
    print('Visualise has run successfully.')


def offset_mean(data, target_mean_value=0):
    """JT - Internal comments like this are shown in the help fnction for the
    function. Also, defining the tmv as = 0 sets it as a default value
    meaning we do not also have to define in."""
    return (data - np.mean(data)) + target_mean_value

z = np.zeros((2,2))
print(offset_mean(z, 3))

#visualise(r"C:\Users\James\Desktop\swc-python\python-novice-inflammation-data\data\inflammation-01.csv")

# help(np.loadtxt)

def fence(original, wrapper):
    """JT - Some concatenation practice..."""
    return wrapper + original + wrapper

print(fence('name', '*'))


def rescale(array):
    scaled = (array - np.amin(array))/(np.amax(array)-np.amin(array))
    return scaled

nums = [1, 2, 3]

print(rescale(nums))
