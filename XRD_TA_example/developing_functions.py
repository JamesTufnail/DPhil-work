import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
