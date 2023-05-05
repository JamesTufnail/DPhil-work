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

def indexing_and_slicing(filename):
    """JT - This function takes a PPMS file, indexes the locations of the changes of sweep rate,
    then slices and appends new columns for each sweep rate for the DC Moment and Magnetic Field.
    It then saves an excel file with the new data."""

    ## TODO: Add the labels of each sweep rate as a header for each column.

    data = pd.read_csv(filename, skiprows=33)
    data_df = pd.DataFrame(data, columns=['Comment', 'Magnetic Field (Oe)', 'DC Moment (emu)'])

    ## this works to find the indices that the sweep rate changes at
    indices = []
    for index, comment in enumerate(data_df["Comment"]):
        if isinstance(comment, str) and "Ramp" in comment:
            indices.append(index)

    # This works for slicing the columns up into the right numbers of moment and field

    moment, field = [], []

    for i, row in enumerate(indices):
        if i < len(indices) - 1:
            data_df["New Moment {}".format(i)] = data_df["DC Moment (emu)"][indices[i]:indices[i + 1] - 1]
            data_df["New Field {}".format(i)] = data_df["Magnetic Field (Oe)"][indices[i]:indices[i + 1] - 1]
        elif i == len(indices) - 1:
            data_df["New Moment {}".format(i)] = data_df["DC Moment (emu)"][indices[i]:]
            data_df["New Field {}".format(i)] = data_df["Magnetic Field (Oe)"][indices[i]:]

    # data_df.to_excel("sliced_data_{}.xlsx".format(filename), index=False)
    print('Indexing and slicing has successfully run.')