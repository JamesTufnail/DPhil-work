import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def field_moment_plot(filename):
    """ JT - Function takes data file names, reads csv file from PPMS data, ignoring first 33 lines (preamble)
     and plots magnetic field against DC moment"""
    ## TODO: convert from DC Moment into magnetic moment (A m^2), update marker, plot all on one figure, fix titles

    data = pd.read_csv("{}".format(filename), skiprows=33)

    data["Magnetic Field (T)"] = data["Magnetic Field (Oe)"] * 0.0001

    plt.scatter(data["Magnetic Field (T)"], data["DC Moment (emu)"], marker=1)
    plt.title('{}'.format(filename[-12:-4]))
    plt.xlabel('Magnetic Field (T)')
    plt.ylabel('DC Moment (emu)')

    plt.show()
    print('Field_moment_plot has run successfully.')
