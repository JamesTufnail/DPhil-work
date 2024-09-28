import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
Script for plotting the shift in each peak centre in YBCO (Cu, in/out of phase O, O4)
"""

peaks = ['Cu', 'out-phase', 'in-phase', 'O4']

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(8, 6))

# Flatten the axs array to make it easier to iterate through
axs = axs.flatten()

for peak, ax in zip(peaks,axs):

    p = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Experimental Peak Values - 810YBCO.xlsx",
                      sheet_name=peak) # Change the sheet name to select different peak to plot
    title = '{} Peak'.format(peak)

    print(p)

    # Sample data
    x_labels = ["Pristine", "300 keV", "Annealed"]  # The x-values for each set of y-values
    x = [1,2,3]

    # y_values = [
    #     p["Pristine"],  # First set of y-values (corresponding to x=1)
    #     p["Irr"],  # Second set of y-values (corresponding to x=2)
    #     p["Annealed"],  # Third set of y-values (corresponding to x=3)
    # ]
    #
    # y_errors = [
    #     p["Pri Error"],  # First set of y-values (corresponding to x=1)
    #     p["Irr Error"],  # Second set of y-values (corresponding to x=2)
    #     p["Ann Error"],  # Third set of y-values (corresponding to x=3)
    # ]


    for i, (y_vals, y_errs, label) in enumerate(zip(y_values, y_errors, x_labels), start=1):
        x_coords = np.full_like(y_vals, x[i-1])  # Repeat the same x value for each y in this group
        # plt.scatter(x_coords, y, label=label)
        ax.errorbar(x_coords, y_vals, yerr=y_errs, fmt='o', capsize=5, markersize=5, label=label)

    ax.set_title(title)
    ax.set_xticks(range(1, len(x_labels) + 1))
    ax.set_xticklabels(x_labels, rotation=45)
    ax.grid(True)

# Create a common legend for all subplots
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')

# Add an overall title to the plot
fig.suptitle('Peak Shifts in 810YBCO Thin Film', fontsize=16)

# Set common x-axis and y-axis labels for the entire figure
fig.text(0.05, 0.5, 'Wavenumber (cm$^{-1}$)', ha='center', va='center', rotation='vertical', fontsize=12)



plt.subplots_adjust(hspace=0.5)
plt.show()