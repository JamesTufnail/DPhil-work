import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## TODO: field_moment_plot: update marker, plot all on one figure, fix titles


def field_moment_plot(filename):
    """ JT - Function takes data file names, reads csv file from PPMS data, ignoring first 33 lines (preamble)
     and plots magnetic field against DC moment"""

    data = pd.read_csv("{}".format(filename), skiprows=33)
    plt.scatter(data["Magnetic Field (Oe)"], data["DC Moment (emu)"], marker=1)

    plt.title('{}'.format(filename[-12:-4]))
    plt.xlabel('Magnetic Field (Oe)')
    plt.ylabel('DC Moment (emu)')

    plt.show()
    print('Field_moment_plot has run successfully for ...{}.'.format(filename[-25:]))
