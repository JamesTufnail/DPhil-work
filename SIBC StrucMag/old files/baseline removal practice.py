
import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import pandas as pd
from scipy.signal import savgol_filter
import sklearn.linear_model as lm
from sklearn.preprocessing import PolynomialFeatures
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks

from pybaselines import Baseline, utils


label = 'SP11-SM3c'
file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\SP11-SM3c-532nm.txt"

# read in data and separate into wavenumber and intensity
data = pd.read_table(file, delimiter = '\t', header = 12, skiprows=20)
data.columns = ['Wavenumber', 'Intensity']
wavenumber, intensity = data['Wavenumber'], data['Intensity']

# Filter data where 'Wavenumber' is below 75
filtered_data = data[data['Wavenumber'] >= 65]

# Extract the filtered 'Wavenumber' and 'Intensity' columns
wavenumber, intensity = filtered_data['Wavenumber'], filtered_data['Intensity']

# using baseline fiter function from pybaselines
baseline_fitter = Baseline(x_data=wavenumber)

# fit the baseline in different ways
bkg1, params1 = baseline_fitter.modpoly(intensity, poly_order=4)
bkg_2, params_2 = baseline_fitter.asls(intensity, lam=1e7, p=0.02)
bkg_3, params_3 = baseline_fitter.mor(intensity, half_window=30)
bkg_4, params_4 = baseline_fitter.snip(
    intensity, max_half_window=40, decreasing=True, smooth_half_window=3
)


# plot the data
plt.plot(wavenumber, intensity, label='Raw Data')
plt.plot(wavenumber, bkg1, '--', label='Modpoly baseline')
plt.plot(wavenumber, bkg_2, '--', label='asls')
plt.plot(wavenumber, bkg_3, '--', label='mor')
plt.plot(wavenumber, bkg_4, '--', label='snip')

plt.legend()
plt.show()



# Create the subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot on each subplot
axs[0, 0].plot(wavenumber, intensity, label='Raw Data')
axs[0, 0].plot(wavenumber, bkg1, '--', label='Modpoly baseline')
axs[0, 0].legend()
axs[0, 0].set_title('Modpoly Baseline')

axs[0, 1].plot(wavenumber, intensity, label='Raw Data')
axs[0, 1].plot(wavenumber, bkg_2, '--', label='ASLS')
axs[0, 1].legend()
axs[0, 1].set_title('ASLS Baseline')

axs[1, 0].plot(wavenumber, intensity, label='Raw Data')
axs[1, 0].plot(wavenumber, bkg_3, '--', label='MOR')
axs[1, 0].legend()
axs[1, 0].set_title('MOR Baseline')

axs[1, 1].plot(wavenumber, intensity, label='Raw Data')
axs[1, 1].plot(wavenumber, bkg_4, '--', label='SNIP')
axs[1, 1].legend()
axs[1, 1].set_title('SNIP Baseline')

# Set a common x and y label
for ax in axs.flat:
    ax.set_xlabel('Wavenumber')
    ax.set_ylabel('Intensity')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Subtracting background ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
modpoly_subtracted = intensity - bkg1
asls_subtracted = intensity - bkg_2
mor_subtracted = intensity - bkg_3
snip_subtracted = intensity - bkg_4

# Plot the subtracted data on one plot
plt.plot(wavenumber, modpoly_subtracted, label='Modpoly baseline')
plt.plot(wavenumber, asls_subtracted, label='ASLS')
plt.plot(wavenumber, mor_subtracted, label='MOR')
plt.plot(wavenumber, snip_subtracted, label='SNIP')
plt.legend()
plt.xlabel('Wavenumber')
plt.ylabel('Intensity')
plt.title('Subtracted Baselines Comparisons')
plt.show()


# subtracted data on subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot on each subplot
axs[0, 0].plot(wavenumber, modpoly_subtracted, label='Modpoly baseline')
axs[0, 0].set_title('Modpoly Baseline')

axs[0, 1].plot(wavenumber, asls_subtracted, label='ASLS')
axs[0, 1].set_title('ASLS Baseline')

axs[1, 0].plot(wavenumber, mor_subtracted,  label='MOR')
axs[1, 0].set_title('MOR Baseline')

axs[1, 1].plot(wavenumber, snip_subtracted, label='SNIP')
axs[1, 1].set_title('SNIP Baseline')

# Set a common x and y label
for ax in axs.flat:
    ax.set_xlabel('Wavenumber')
    ax.set_ylabel('Intensity')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()