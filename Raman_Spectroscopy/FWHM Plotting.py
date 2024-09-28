import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Code currently to plot the shifts in FWHM
p = pd.read_excel(r"",
                  sheet_name='') # Change the sheet name to select different peak to plot
title = 'FWHM Shift in Cu Peak'

# Sample data
x_labels = ["Pristine", "300 keV", "Annealed"]  # The x-values for each set of y-values
x = [1,2,3]

y_values = [
    p["Pristine"],  # First set of y-values (corresponding to x=1)
    p["Irradiated"],  # Second set of y-values (corresponding to x=2)
    p["Annealed"],  # Third set of y-values (corresponding to x=3)
]


y_errors = [
    p["Pri Error"],  # First set of y-values (corresponding to x=1)
    p["Irr Error"],  # Second set of y-values (corresponding to x=2)
    p["Ann Error"],  # Third set of y-values (corresponding to x=3)
]

plt.figure(figsize=(4,4))

for i, (y_vals, y_errs, label) in enumerate(zip(y_values, y_errors, x_labels), start=1):
    x_coords = np.full_like(y_vals, x[i-1])  # Repeat the same x value for each y in this group
    # plt.scatter(x_coords, y, label=label)
    plt.errorbar(x_coords, y_vals, yerr=y_errs, fmt='o', capsize=5, markersize=5, label=label)


plt.ylabel('Wavenumber')
plt.title(title)
plt.xticks(range(1, len(x_labels) + 1), x_labels) # Swapping numeric x values for labels
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.legend()
plt.tight_layout()  # Ensure the labels are not cut off
plt.show()