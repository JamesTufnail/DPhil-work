import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
################################################### Functions and Params ########################################################################
def annotate_raman_peaks(verticals, labels, annotate_height):
    """ Function to annotate the raman peaks on a plot

    :param verticals: Boolean to plot verticals
    :param labels: Boolean to plot labels
    :param annotate_height: Height of the annotation
    :return: None"""

    # plotting verticals
    if verticals == 'True':
        plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
        plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')

    # Adding annotation arrows for known peaks
    if labels == 'True':
        plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
                    arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('Cu(2)', xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 0.5),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height +0.5),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

annotate_height = 3 # Height of annotation text

# Inputting YBCO peaks from pristine sample
Ba_freq = 107.5
Cu2_freq = 145.9
O2_O3_freq1 = 331.7
O2_O3_freq2 = 433.5
O4_freq = 496.8

############################################### Script ################################################################

# Reading in raw file names
files = [
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\PristineY\cropped and subbed\Fu21Y_p_5point_avg.txt", delimiter=' ', names=['Wavenumber', 'Counts']),
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\Fu21Y_1_300_kev_He\cropped and subbed\Fu21Y_300keV_He_5point_avg.txt", delimiter=' ', names=['Wavenumber', 'Counts']),
        pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\2MeV O\cropped and subbed\Fu21Y_2MeV_O_5point_avg.txt", delimiter=' ', names=['Wavenumber', 'Counts']),
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


title = "Fu21Y Cascade Plot"

shifts = range(len(files))

for file, index, label in zip(files, shifts, labels):
        wavenumber, counts = file['Wavenumber'], file['Counts']
        plt.scatter(wavenumber, counts + 1*index, s = 0.5, label = label)

for fitted_file, index, label in zip(fitted_files, shifts, fitted_labels):
        fitted_wavenumber, fitted_counts = fitted_file['Wavenumber'], fitted_file['Counts']
        plt.plot(fitted_wavenumber, fitted_counts + 1*index, label = label)

annotate_raman_peaks('True', 'False', annotate_height)
plt.xlim(100, 700)
plt.title(title, fontsize = 16)
plt.xlabel('Wavenumber (cm$^{-1}$)', fontsize=12)
plt.ylabel('Normalized Counts', fontsize=12)
plt.legend()
plt.show()
