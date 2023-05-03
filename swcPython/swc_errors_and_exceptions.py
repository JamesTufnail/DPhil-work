import matplotlib.pyplot as plt
import numpy as np

def plot_scatter(filename, title, x_axis, y_axis):
    """JT - general scatter plotting function.
    Inputs: filename, title, x_axis, y_axis"""
    data = np.loadtxt(fname=filename, delimiter=',')

    plt.scatter(data)

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)

    plt.show()
    print('Scatter function has run succesfully for {}.'.format(filename))

