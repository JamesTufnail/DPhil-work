"""
Author: James Tufnail
Date: July 2024

Quick script to plot a single XRD spectrum with or without a SNIP baseline

"""
import matplotlib.pyplot as plt
import pandas as pd
from pybaselines import Baseline, utils
from scipy.signal import find_peaks
import numpy as np

sample = 'Cu Metal'
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\XRD\Cu-and-cuo\CuO_powder_spinner_gonio_v1.csv",
                   delimiter = ',', header=25)


angle, intensity = data['Angle'], data['Intensity']
root_intensity = [i**0.5 for i in intensity]

# using baseline fitter function from pybaselines to fit a snip baseline
baseline_fitter = Baseline(x_data=angle)
bkg, params = baseline_fitter.snip(root_intensity, max_half_window=50, decreasing=True, smooth_half_window=3)

# plot the data
plt.plot(angle, root_intensity, label = 'Raw Data')
plt.plot(angle, bkg, '--', label='Baseline')

# add labels and title
plt.xlabel('2$\\theta$ (degrees)')
plt.ylabel(r'$\sqrt{Intensity}$ $(\sqrt{cps})$')
plt.title('Goniometer scan of {}'.format(sample))
plt.legend()
plt.show()
# plt.savefig(r'C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\gonio figures' + '\\' + sample + ' baseline.png')
# plt.close()


"""temporarily comemnted below code because I don't want to remove the baseline"""
# subtract the baseline from the raw data
# corrected_intensity = root_intensity - bkg

# prominence = 3
# height = 0.5
# # find peaks and plot crosses at peak locations from smoothed data
# peaks_ix, _ = find_peaks(corrected_intensity, prominence=prominence, height=height)
# peaks_x, peaks_y = angle[peaks_ix], corrected_intensity[peaks_ix]
# peak_pos = peaks_x[:].tolist()
# print('Peak positions are: \n', peak_pos)

# # plot the corrected data
# plt.plot(angle, corrected_intensity, label='Corrected Data')
# # plt.plot(peaks_x, peaks_y, "x")
# plt.axhline(0, color='grey', linestyle='--')

# plt.xlabel('2$\\theta$ (degrees)')
# plt.ylabel(r'$\sqrt{Intensity}$ $\sqrt{cps}$')
# plt.title('C-axis goniometer scan of {} with baseline removed'.format(sample))

# # plt.savefig(r'C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\gonio figures' + '\\' + sample + ' corrected.png')
# plt.close()
# # plt.show()


# # normalise data and create dataframe 

# # normalise the corrected data
# normalised_intensity = np.interp(corrected_intensity, (corrected_intensity.min(), corrected_intensity.max()), (0, 1))
# final_df = pd.DataFrame({'Angle': angle, 'Intensity': normalised_intensity})
# final_df.reset_index(drop=True, inplace=True)
# print(final_df.head()) # Print the first few rows of the DataFrame
# final_df.to_csv('processed_XRD_spectra' + '\\' + sample + '_processed.csv', index=False)