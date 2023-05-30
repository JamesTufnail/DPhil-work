import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import log10, floor

def final_raw_mawatari(data, indices, position):
    """ JT - This functino should take the dataframe from the file, then use the indices found from FIND_INDICES to
    plot the multiple sweep rates on one plot. It should use the position input to position everything on a
    large figure itself"""
    ## TODO: generalise this to plot all files from one sample as subplots in a massive figure

    # Converting the units
    data["Magnetic Field (T)"] = data["Magnetic Field (Oe)"] * 0.0001
    data["Magnetic Moment (A m^2)"] = data["DC Moment (emu)"] * 0.001

    n_rows = 2
    n_cols = 3
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(3 * n_cols, 4 * n_rows))
    ax = axes[position]

    # Plotting for multiple sweep rates depending on the index
    for new_sweep_row in range(len(indices) - 1):
        start_row = indices[new_sweep_row]
        end_row = indices[new_sweep_row + 1] - 1
        # print(start_row, end_row)
        ax.scatter(data.iloc[start_row:end_row, 3], data.iloc[start_row:end_row, 4],
                   label='Sweep Rate {}'.format(start_row), s=10)
        plt.legend()
    plt.show()

    print('multiple_raw_mawatari has run successfully.')


# n_files = len(mawatari_files)
# if n_files % 2 == 0:
#     n_rows = n_files / 2
#     n_cols = n_files / n_rows
# elif n_files % 2 == 1:
#     n_rows = (n_files % 2)
#     n_cols = n_rows + 1
#
# fig, axes = plt.subplots(nrows = n_rows, ncols = n_cols, figsize=(3*n_files, 4))


## TODO: finish this as a susceptibility plot and check its actually plotting the right susceptibility with Simon,
## TODO: write it into a function that can take any file


def magnetisation_measurements(data, indices):
    """JT - This function takes a dataframe and indices values (from find_field_start). It then plots the first
    second derivative of AC magnetic susceptiblity as a fucntion of temperature for multiple magnetic fields.
    INPUTS: data (dataframe), indices (array of indices of rows where applied field changes)
    OUPUTS: 2x1 scatter plots.
    """
    # Setting up figure
    fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1, figsize=(8, 5))

    # Converting the units
    data["Magnetic Field (T)"] = data["Magnetic Field (Oe)"] * 0.0001

    for new_magnetic_field in range(len(indices) - 1):
        start_row = indices[new_magnetic_field]
        end_row = indices[new_magnetic_field + 1] - 1

        #print('Start row is {}'.format(start_row))
        #print('End row is {}'.format(end_row))

        # Extracting label for Field strength from dataframe,
        label = data.loc[start_row, "Magnetic Field (T)"]
        rounded_label = round(label, 2-int(floor(log10(abs(label))))-1)

        ax1.scatter(data["Temperature (K)"][start_row:end_row], data[r'AC X" (emu/Oe)'][start_row:end_row],
                    label='{} T'.format(rounded_label), s=10)
        ax2.scatter(data["Temperature (K)"][start_row:end_row], data["AC X'  (emu/Oe)"][start_row:end_row],
                label='{} T'.format(rounded_label), s=10)

    plt.legend()
    plt.show()


def find_field_start(filename):
    """JT - This function takes a PPMS file and finds the indices at which the magnetic field changes.
        OUTPUTS: indices, data_df.
        NOTE: this is basically the sanme as find_ramp_start just using a different search term"""
 ## TODO: currently this misses that alst 200 rows (H = 14 T)


    data = pd.read_csv(filename, skiprows=33)
    data_df = pd.DataFrame(data, columns=['Comment', "Temperature (K)", 'Magnetic Field (Oe)', r'AC X" (emu/Oe)', "AC X'  (emu/Oe)", ])

    ## this works to find the indices that the sweep rate changes at
    indices = []
    for index, comment in enumerate(data_df["Comment"]):
        if isinstance(comment, str) and "sample offset" in comment:
            indices.append(index)
    return indices, data_df