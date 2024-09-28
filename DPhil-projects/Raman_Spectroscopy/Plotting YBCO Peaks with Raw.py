import pandas as pd
import matplotlib.pyplot as plt

"""
Script to plot each individual YBCO peak (Cu, in-phase O, out of phase O, O4)
"""

peaks = ['Cu', 'Out-of-phase', 'In-phase', 'O4']
x_lims = [
    [125, 180],
    [300, 390],
    [420, 480],
    [400, 600],
]

y_lims = [
    [0, 2],
    [0, 1.5],
    [0, 1.5],
    [0, 1.5],
]

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
axs = axs.flatten()

# Reading in raw file names
files = [
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated "
                    r"Conductors\Fu21Y\PristineY\cropped and subbed\Fu21Y_p_5point_avg.txt", delimiter=' ',
                    names=['Wavenumber', 'Counts']),
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated "
                    r"Conductors\Fu21Y\Fu21Y_1_300_kev_He\cropped and subbed\Fu21Y_300keV_He_5point_avg.txt",
                    delimiter=' ', names=['Wavenumber', 'Counts']),
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated "
                    r"Conductors\Fu21Y\2MeV O\cropped and subbed\Fu21Y_2MeV_O_5point_avg.txt", delimiter=' ',
                    names=['Wavenumber', 'Counts']),
]
# Labelling raw file names
labels =[
        'Pristine',
        '300 keV He$^+$',
        '2 MeV O$^+$',
]

# Reading in fitted file names
fitted_files = [
        pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\Fu21Y_origin_fitted.xlsx", sheet_name='Fu21Y_p'),
        pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\Fu21Y_origin_fitted.xlsx", sheet_name='Fu21Y_300keV_He'),
        pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\Fu21Y_origin_fitted.xlsx", sheet_name='Fu21Y_2MeV_O'),
]
# Labelling fitted file names
fitted_labels = [
        'Pristine Fit',
        '300 keV He$^+$ Fit',
        '2 MeV O$^+$ Fit',
]

shifts = range(len(files))

for file, index, label in zip(files, shifts, labels):
        wavenumber, counts = file['Wavenumber'], file['Counts']
        axs[0].scatter(wavenumber, counts + 0.5 * index, s = 0.5, label=label)
        axs[1].scatter(wavenumber, counts + 0.5 * index, s=0.5, label=label)
        axs[2].scatter(wavenumber, counts + 0.5 * index, s=0.5, label=label)
        axs[3].scatter(wavenumber, counts + 0.5 * index, s=0.5, label=label)

for fitted_file, index, fitted_label in zip(fitted_files, shifts, fitted_labels):
        fitted_wavenumber, fitted_counts = fitted_file['Wavenumber'], fitted_file['Counts']
        axs[0].plot(fitted_wavenumber, fitted_counts + 0.5 * index, label = fitted_label)
        axs[1].plot(fitted_wavenumber, fitted_counts + 0.5 * index, label=fitted_label)
        axs[2].plot(fitted_wavenumber, fitted_counts + 0.5 * index, label=fitted_label)
        axs[3].plot(fitted_wavenumber, fitted_counts + 0.5 * index, label=fitted_label)

for i, (x_lim, y_lim) in enumerate(zip(x_lims, y_lims)):
    axs[i].set_xlim(x_lim[0], x_lim[1])
    axs[i].set_ylim(y_lim[0], y_lim[1])

for i, title in enumerate(peaks):
    axs[i].set_title(title + ' Peak')
    axs[i].grid('True')

fig.suptitle('Peak Shifts in 810YBCO Thin Film', fontsize=16)

# Set common x-axis and y-axis labels for the entire figure
fig.text(0.5, 0.06, 'Wavenumber (cm$^{-1}$)', ha='center', va='center', fontsize=12)
fig.text(0.06, 0.5, 'Intensity (arb. units)', ha='center', va='center', rotation='vertical', fontsize=12)

# Set common legend for all subplots
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')
plt.show()
