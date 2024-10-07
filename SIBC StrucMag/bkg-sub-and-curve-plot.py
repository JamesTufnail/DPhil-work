"""
Script to plot the processed (i.e. background subtracted) Raman spectra and the fitted data.

Inputs:
    - Data file containing the processed Raman spectra
    - Data file containing the fitted data (exported from Fityk as: 'x', 'y', 'F[n](x)','F(x)')

Outputs:
    - Plot of the processed data and the fitted data

"""
# import libraries
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
import numpy as np
import os

save = False
""" Edit the title, data and fit_data paths """
# title = 'SP11-SM 532nm Pristine'
# data = r"C:\Users\James\coding-projects\DPhil-projects\SIBC StrucMag\baseline-removed-files\pristine\csv-files\SP11-SM 532nm Pristine-snip-subtracted-data.csv"
# fit_data = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Raman\Pristine Raman Data\fityk-fitted-peaks\SP11-SM 532nm Pristine-snip-subtracted-data.dat"
# processed_data = pd.read_csv(data, sep = ',')
# fit = pd.read_csv(fit_data, sep=' ', header = None, names = ['x', 'y', 'F[0](x)', 'F[1](x)', 'F[2](x)', 'F[3](x)', 'F[4](x)', 'F[5](x)', 'F[6](x)', 'F[7](x)', 'F[8](x)', 'F[9](x)', 'F[10](x)', 'F(x)'])

title = 'SuNAM21Gd-SM 532nm Pristine'
data = r"C:\Users\James\coding-projects\DPhil-projects\SIBC StrucMag\baseline-removed-files\pristine\csv-files\SuNAM21Gd-SM 532nm Pristine-snip-subtracted-data.csv"
fit_data = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Raman\Pristine Raman Data\fityk-fitted-peaks\SuNAM21Gd-SM 532nm Pristine-snip-subtracted-data.dat"
processed_data = pd.read_csv(data, sep = ',')
fit = pd.read_csv(fit_data, sep=' ', header = None, names = ['x', 'y', 'F[0](x)', 'F[1](x)', 'F[2](x)', 'F[3](x)', 'F[4](x)', 'F[5](x)', 'F[6](x)', 'F(x)'])




print(fit)
print(processed_data.head())

" ~~~~ Don't edit below this line ~~~~~ "
img_dir = r'C:\Users\James\coding-projects\DPhil-projects\SIBC StrucMag\final-fitted-figures'
wavenumber, intensity = processed_data['Wavenumber'], processed_data['Intensity']
fit_wavenumber, fit_sum = fit['x'], fit['F(x)']

# extract peak position
num_peaks = len(fit.columns) - 3
peaks = [] 
for i in range(num_peaks):
    peak = fit[f'F[{i}](x)'].idxmax()
    peaks.append(fit['x'][peak])
peaks.sort()
print(f"Peak locations are {peaks}")


# Generate a colormap with 12 colors
viridis = cm.get_cmap('viridis', 12)

# Select evenly spaced colors from the colormap (num_peaks +1 is the number of peaks + the sum of the fits)
colors = viridis(np.linspace(0, 1, num_peaks+1))

plt.figure(figsize=(12,6))

# plotting background subtracted and fitted data
plt.scatter(wavenumber, intensity, s=5, label = 'Processed Data', color='grey')
plt.plot(fit_wavenumber, fit_sum, label='Sum of Fits', color=colors[0])

# Plot individual peaks with the remaining colors
for i in range(num_peaks):
    plt.plot(fit_wavenumber, fit[f'F[{i}](x)'], label=f'Peak centre = {peaks[i]:.0f} cm$^{{-1}}$', color=colors[i+1])

# format figure
plt.ylabel('Normalised Intensity (a.u.)', fontsize='large')
plt.yticks([])
plt.xlabel('Wavenumber ($cm^{-1}$)', fontsize='large')
plt.legend()
plt.xlim(50, 800)
plt.title(title)

if save:
    plt.savefig(os.path.join(img_dir, f'{title}-processed-and-fitted.png'))
    plt.close()
else:
    plt.show()