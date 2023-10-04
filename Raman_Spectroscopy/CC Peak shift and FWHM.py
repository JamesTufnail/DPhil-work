import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x_labels = ["Pristine", "300 keV He", "2 MeV O"]

Cu_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
Cu1_O1_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
Out_of_phase_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

################ Peak Centres #################
# Cu_vals = [145.9, 136.3, 137.0]
# Cu_errors = [0.575, 0.575, 0.575]
#
# Cu1_O1_vals = [231.0, 223.0, 222.0]
# Cu1_O1_errors = [0.575, 0.635, 0.636]
#
# Out_of_phase_vals = [331.7, 325.9, 327.4]
# Out_of_phase_errors = [0.575, 0.575, 0.575]

################ FWHM #################
Cu_vals = [12.3, 22.7, 32.5]
Cu_errors = [0.575, 0.575, 0.575]

Cu1_O1_vals = [22.7, 35.7, 36.0]
Cu1_O1_errors = [0.575, 1.184, 2.297]

Out_of_phase_vals = [21.3, 22.3, 20.4]
Out_of_phase_errors = [0.575, 0.678, 0.596]





fig, axs = plt.subplots(1, 3, figsize=(8, 4))  # Create a 2x1 grid of subplots

# First subplot
for i in range(len(Cu_vals)):
    axs[0].errorbar(i + 1, Cu_vals[i], yerr=Cu_errors[i], fmt='o', capsize=5, markersize=5, color=Cu_colors[i], label='Cu')
axs[0].set_xticks(range(1, len(x_labels) + 1))
axs[0].set_xticklabels(x_labels, rotation=45)
axs[0].set_ylabel('Wavenumber (cm$^{-1}$)')
axs[0].set_title('Cu2 Mode')
axs[0].set_xlim(0.5, 3.5)

# Second subplot
for i in range(len(Cu1_O1_vals)):
    axs[1].errorbar(i + 1, Cu1_O1_vals[i], yerr=Cu1_O1_errors[i], fmt='o', capsize=5, markersize=5, color=Cu1_O1_colors[i], label='Cu1_O1')
axs[1].set_xticks(range(1, len(x_labels) + 1))
axs[1].set_xticklabels(x_labels, rotation=45)
axs[1].set_title('Cu1-O1 Mode')
axs[1].set_xlim(0.5, 3.5)

# Third subplot
for i in range(len(Out_of_phase_vals)):
    axs[2].errorbar(i + 1, Out_of_phase_vals[i], yerr=Out_of_phase_errors[i], fmt='o', capsize=5, markersize=5, color=Out_of_phase_colors[i], label='Out_of_phase')
axs[2].set_xticks(range(1, len(x_labels) + 1))
axs[2].set_xticklabels(x_labels, rotation=45)
axs[2].set_title('Out-of-phase Oxygen Mode')
axs[2].set_xlim(0.5, 3.5)

# Adjust layout to prevent overlap
plt.tight_layout()
# fig.suptitle('Raman Peak Shifts in Pristine and Irradiated YBCO', fontsize=16)
# handles, labels = axs[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper right')

plt.show()

