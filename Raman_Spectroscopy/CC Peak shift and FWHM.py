import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Cu_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#c32148']
Cu1_O1_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#c32148']
Out_of_phase_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#c32148']
O4_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#c32148']

################ Peak Centres for Fu21Y_area #################
# x_labels = ["Pristine", "2 MeV O (20.2)", "300 keV He (39.0)"]
# lim = [0.5, 3.5]

# Cu_vals = [139.7, 137.0, 135.4]
# Cu_errors = [0.575, 0.575, 0.575]

# Cu1_O1_vals = [228.5, 222.0, 224.0]
# Cu1_O1_errors = [0.575, 0.636, 0.635]

# Out_of_phase_vals = [331.0, 327.4, 325.5]
# Out_of_phase_errors = [0.575, 0.575, 0.575]

# O4_vals = [480.5, 469.6, 460.9]
# O4_errors = [0.742, 1.091, 1.149]

################ FWHM for Fu21Y_area #################
# x_labels = ["Pristine", "2 MeV O (20.2)", "300 keV He (39.0)"]
# lim = [0.5, 3.5]

# Cu_vals = [21.5, 32.54, 24.4]
# Cu_errors = [0.575, 0.575, 0.575]

# Cu1_O1_vals = [24.7, 36.0, 41.5]
# Cu1_O1_errors = [2.302, 2.297, 2.038]

# Out_of_phase_vals = [26.0, 20.4, 24.49]
# Out_of_phase_errors = [0.925, 0.596, 0.575]

# O4_vals = [68.1, 65.9, 48.9]
# O4_errors = [3.452, 3.609, 3.614]

################ Peak Centre for Fu21Gd_area #################
# x_labels = ["Pristine", "2 MeV O (20.2)",  "2 MeV He (23.7)", "300 keV He (39.0)"]
# lim = [0.5, 4.5]

# Cu_vals = [137.8, 135, 134.8, 133.8]
# Cu_errors = [0.575, 0.575, 0.575, 0.575]

# Cu1_O1_vals = [225.4, 218.1, 219.9, 218.2]
# Cu1_O1_errors = [0.575, 0.575, 0.748, 0.617]

# Out_of_phase_vals = [322.6, 316.4, 316.5, 318.0]
# Out_of_phase_errors = [0.575, 0.575, 0.575, 0.575]

# O4_vals = [480, 457, 466.8, 464]
# O4_errors = [0.840, 0.695, 1.317, 1.502]

################ FWHM for Fu21Gd_area #################
x_labels = ["Pristine", "2 MeV O (20.2)",  "2 MeV He (23.7)", "300 keV He (39.0)"]
lim = [0.5, 4.5]

Cu_vals = [18, 18, 20, 25]
Cu_errors = [0.575, 0.575, 0.575, 0.828]

Cu1_O1_vals = [24.6, 26.7, 27.7, 30.4]
Cu1_O1_errors = [1.477, 1.427, 2.801, 2.270]

Out_of_phase_vals = [31.7, 27.4, 30.9, 24.7]
Out_of_phase_errors = [0.694, 0.647, 0.824, 0.839]

O4_vals = [61, 43.6, 62.6, 31]
O4_errors = [3.173, 2.64, 5.786, 5.09]


fig, axs = plt.subplots(1, 4, figsize=(12, 4))  # Create a 2x1 grid of subplots

# First subplot
for i in range(len(Cu_vals)):
    axs[0].errorbar(i + 1, Cu_vals[i], yerr=Cu_errors[i], fmt='o', capsize=5, markersize=5, color=Cu_colors[i], label='Cu')
axs[0].set_xticks(range(1, len(x_labels) + 1))
axs[0].set_xticklabels(x_labels, rotation=45)
axs[0].set_ylabel('Wavenumber (cm$^{-1}$)')
axs[0].set_title('Cu2 Mode')
axs[0].set_xlim(lim[0], lim[1])

# Second subplot
for i in range(len(Cu1_O1_vals)):
    axs[1].errorbar(i + 1, Cu1_O1_vals[i], yerr=Cu1_O1_errors[i], fmt='o', capsize=5, markersize=5, color=Cu1_O1_colors[i], label='Cu1_O1')
axs[1].set_xticks(range(1, len(x_labels) + 1))
axs[1].set_xticklabels(x_labels, rotation=45)
axs[1].set_title('Cu1-O1 Mode')
axs[1].set_xlim(lim[0], lim[1])

# Third subplot
for i in range(len(Out_of_phase_vals)):
    axs[2].errorbar(i + 1, Out_of_phase_vals[i], yerr=Out_of_phase_errors[i], fmt='o', capsize=5, markersize=5, color=Out_of_phase_colors[i], label='Out_of_phase')
axs[2].set_xticks(range(1, len(x_labels) + 1))
axs[2].set_xticklabels(x_labels, rotation=45)
axs[2].set_title('Out-of-phase Oxygen Mode')
axs[2].set_xlim(lim[0], lim[1])

for i in range(len(O4_vals)):
    axs[3].errorbar(i + 1, O4_vals[i], yerr=O4_errors[i], fmt='o', capsize=5, markersize=5, color=O4_colors[i], label='O4')
axs[3].set_xticks(range(1, len(x_labels) + 1))
axs[3].set_xticklabels(x_labels, rotation=45)
axs[3].set_title('Oxygen 4 Mode')
axs[3].set_xlim(lim[0], lim[1])

# 
fig.suptitle('Raman FWHM Change in Pristine and Irradiated Fu21Gd for different damage', fontsize=16, y=0.98)
fig.supxlabel('Sample and damage (mdpa)', fontsize=12)
# fig.ytitle()
# handles, labels = axs[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper right')
plt.tight_layout()
plt.show()

