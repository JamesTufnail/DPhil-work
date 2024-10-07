"""

Uses the snip method to remove background. Based on pybaselines package.
Not actually sure what snip method is but it seemed the best out of some I tried.

Also plots the raw data and the background subtracted data.

Parameters:
-----------
wavenumber : array
    Wavenumber data.
intensity : array
    Intensity data.
    
"""
import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import pandas as pd
from pybaselines import Baseline
import os

title='SuNAM21Gd-SM 532nm Ion1'
data_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Raman\Raman - Ion 1\SuNAM21Gd-ion1\SM2-532nm-overall-avg.txt"

save = True
img_dir = r"C:\Users\James\coding-projects\DPhil-projects\SIBC StrucMag\baseline-removed-files\ion1\figures"
csv_dir = r"C:\Users\James\coding-projects\DPhil-projects\SIBC StrucMag\baseline-removed-files\ion1\csv-files"


""" ~~~~~ Don't edit below this line ~~~~~ """
# load data
data = pd.read_csv(data_path, header = 11, sep = '\t', names = ['Wavenumber', 'Intensity'])
print(data.head()) 

# Filter data where 'Wavenumber' is below 75
filtered_data = data[data['Wavenumber'] >= 75]

# Extract the filtered 'Wavenumber' and 'Intensity' columns
wavenumber, intensity = filtered_data['Wavenumber'], filtered_data['Intensity']

# plot raw data
plt.scatter(wavenumber, intensity, s=5)
plt.title(f'Raw {title}')
plt.xlabel('Wavenumber')
plt.ylabel('Intensity (CCD counts)')

if save:
    plt.savefig(os.path.join(img_dir, f'{title}-raw-plot.png'))
    plt.close()
else:
    plt.show()

# using baseline fiter function from pybaselines
baseline_fitter = Baseline(x_data=wavenumber)

# fit the baseline in different ways
bkg, params = baseline_fitter.snip(intensity, max_half_window=40, decreasing=True, smooth_half_window=3)
snip_subtracted = intensity - bkg

# plot the data
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Plot on each subplot
axs[0].scatter(wavenumber, intensity, s=5, label='Raw Data')
axs[0].plot(wavenumber, bkg, '--', label='SNIP Baseline', color='red')
axs[0].set_title('Raw and SNIP baseline')
axs[0].legend()
axs[0].set_ylabel('Intensity (CCD counts)')

axs[1].scatter(wavenumber, snip_subtracted, s=5, label='Raw Data - SNIP')
# axs[1].axhline(0, color='grey', linestyle='--')
axs[1].set_title('Background subtracted data')
axs[1].set_ylabel('Intensity (a.u.)')
axs[1].set_yticks([])

# Set a common x and y label
for ax in axs.flat:
    ax.set_xlabel('Wavenumber')

# Adjust layout to prevent overlap
plt.suptitle(title)
plt.tight_layout()



# Show the plot
if save:
    plt.savefig(os.path.join(img_dir, f'{title}-bkg-sub-plot.png'))
    plt.close()

    # Construct the save path for the csv file
    save_path = os.path.join(csv_dir, f'{title}-snip-subtracted-data.csv')

    # Export the dataframe to a CSV file
    snip_subtracted_df = pd.DataFrame({'Wavenumber': wavenumber, 'Intensity': snip_subtracted})
    print('Subtracted data:\n', snip_subtracted.head())

    snip_subtracted_df.to_csv(save_path, index=False)
    print(f'Subtracted data saved to: {save_path}')
    
else:
    plt.show()


