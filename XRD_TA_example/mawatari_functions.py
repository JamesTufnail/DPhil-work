import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def undifferentiated_raw_mawatari(filenames):
    """ JT - Function takes data file names, reads csv file from PPMS data, ignoring first 33 lines (preamble)
     and plots magnetic field against DC moment"""

    # reads the number of files to determine number of subplots required
    n_files = len(filenames)
    fig, axes = plt.subplots(nrows=1, ncols=n_files, figsize=(3 * n_files, 4))

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


def multiple_raw_mawatari(data, indices, title):
    """ JT - This functino should take the dataframe from the file, then use the indices found from FIND_INDICES to
    plot the multiple sweep rates on one plot."""

    # Converting the units
    data["Magnetic Field (T)"] = data["Magnetic Field (Oe)"] * 0.0001
    data["Magnetic Moment (A m^2)"] = data["DC Moment (emu)"] * 0.001

    # Plotting for multiple sweep rates depending on the index
    for new_sweep_row in range(len(indices) - 1):
        start_row = indices[new_sweep_row]
        end_row = indices[new_sweep_row + 1] - 1
        # print(start_row, end_row)
        plt.scatter(data.iloc[start_row:end_row, 3], data.iloc[start_row:end_row, 4],
                    label='Sweep Rate {}'.format(start_row), s=10)
        plt.title('{}'.format(title))
        plt.legend()
    plt.show()

    print('multiple_raw_mawatari has run successfully.')

def find_indices(filename):
    """JT - This function takes a PPMS file and finds the indices at which the sweep rate changes.
        OUTPUTS: indices, data_df"""

    data = pd.read_csv(filename, skiprows=33)
    data_df = pd.DataFrame(data, columns=['Comment', 'Magnetic Field (Oe)', 'DC Moment (emu)'])

    ## this works to find the indices that the sweep rate changes at
    indices = []
    for index, comment in enumerate(data_df["Comment"]):
        if isinstance(comment, str) and "Ramp" in comment:
            indices.append(index)
    return indices, data_df

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

    # save sliced data temporarily so that I can call each datafile for plotting in another function!!
    return data_df
    data_df.to_excel("sliced_data.xlsx", index=False)
    print('Indexing and slicing has successfully run.')


