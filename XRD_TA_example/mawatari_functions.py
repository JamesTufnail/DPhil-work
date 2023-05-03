import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def field_moment_plot(filenames):
    """ JT - Function takes data file names, reads csv file from PPMS data, ignoring first 33 lines (preamble)
     and plots magnetic field against DC moment"""
    ## TODO:  update marker, plot all on one neater figure, fix titles

    # reads the number of files to determine number of subplots required
    n_files = len(filenames)
    fig, axes = plt.subplots(nrows=1, ncols=n_files, figsize=(3*n_files, 4))

    for index, file in enumerate(filenames):
        data = pd.read_csv(file, skiprows=33)

        data["Magnetic Field (T)"] = data["Magnetic Field (Oe)"] * 0.0001
        data["Magnetic Moment (A m^2)"] = data["DC Moment (emu)"] * 0.001

        # assigning each subplot its position on the axes
        ax = axes[index]
        ax.plot(data["Magnetic Field (T)"], data["Magnetic Moment (A m^2)"], label='{}'.format(file[-12:-4]))

        # Searching filename for the last occurence of \, to then label it properly
        filename_id = file.rfind('_')
        ax.set_title('{}'.format(file[filename_id + 1:-4]))

    fig.suptitle('Raw Mawatari')
    fig.text(0.5, 0.04, "Magnetic Field (T)", ha="center", va="center")
    fig.text(0.06, 0.5, "DC Moment (A m$^2$)", ha="center", va="center", rotation="vertical")

    plt.tight_layout()
    plt.show()
    print('Field_moment_plot has run successfully for ...{}.'.format(filename[-25:]))
