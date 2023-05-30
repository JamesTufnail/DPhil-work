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


## TODO: finish this as a susceptibility plot and check its actually plotting the right susceptibility with Simon,
## TODO: write it into a function that can take any file
magnetisation_measurements = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron "
                                         r"Irradiation\Birmingham "
                                         r"data\data-for-manipulation-pristine-measurements\Fu21Gdo_1\Irr0\PPMS "
                                         r"Data\22 12 07\Susceptibility_Measurements.csv",
                                         skiprows=33)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 5))
ax1.scatter(magnetisation_measurements["Temperature (K)"][2:233], magnetisation_measurements[r'AC X" (emu/Oe)'][2:233],
            s=10)
ax2.scatter(magnetisation_measurements["Temperature (K)"][2:233], magnetisation_measurements["AC X'  (emu/Oe)"][2:233],
            s=10)
plt.tight_layout
plt.show()