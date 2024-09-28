"""
Raman Analysis Script .v1
James Tufnail
18/07/2024

This script was written to plot and interpret Raman spectra of REBCO samples from my SIBC StrucMag Project.

Stages:
1 - Plot raw data
2 - Drop Rayleigh peak and shorten plot range

"""

import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import pandas as pd
# from scipy.signal import savgol_filter
# import sklearn.linear_model as lm
# from sklearn.preprocessing import PolynomialFeatures
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from lmfit.models import LorentzianModel, VoigtModel, GaussianModel
from pybaselines import Baseline, utils

# ~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~ #

def filter_data(data, wavenumber, intensity, threshold):
    """
    Function to filter data based on a threshold value.
    This is useful to remove low wavenumber rising edge that can interfere with baseline fitting.
    """
    # Filter data where 'Wavenumber' is below 75
    filtered_data = data[data['Wavenumber'] >= threshold]

    # Extract the filtered 'Wavenumber' and 'Intensity' columns
    wavenumber, intensity = filtered_data['Wavenumber'], filtered_data['Intensity']

    return wavenumber, intensity

def normalise_intensity(intensity):
    """
    Function to normalise intensity values between 0 and 1.
    """
    intensity = np.interp(intensity, (intensity.min(), intensity.max()), (0, 1))

    return intensity

def remove_background_snip(wavenumber, intensity, label):
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

    # using baseline fiter function from pybaselines
    baseline_fitter = Baseline(x_data=wavenumber)

    # fit the baseline in different ways
    bkg, params = baseline_fitter.snip(intensity, max_half_window=40, decreasing=True, smooth_half_window=3)
    snip_subtracted = intensity - bkg

    # plot the data
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot on each subplot
    axs[0].plot(wavenumber, intensity, label='Raw Data')
    axs[0].plot(wavenumber, bkg, '--', label='SNIP Baseline')
    axs[0].set_title('Raw and SNIP baseline')
    axs[0].legend()
    
    axs[1].plot(wavenumber, snip_subtracted, label='Raw Data - SNIP')
    axs[1].axhline(0, color='grey', linestyle='--')
    axs[1].set_title('Background subtracted data')

    # Set a common x and y label
    for ax in axs.flat:
        ax.set_xlabel('Wavenumber')
        ax.set_ylabel('Intensity')

    # Adjust layout to prevent overlap
    plt.suptitle(label + ' Pristine')
    plt.tight_layout()


    # Show the plot

    plt.show()

    return wavenumber, snip_subtracted

def raw_raman_simple_plot(files, labels, save_loc, save=False):
    """
    Function to plot raw Raman spectra.
    Option to plot multiple spectra on the same plot.

    Parameters
    files : list of strings
        List of file paths to Raman spectra.
    labels : list of strings
        List of labels for each spectrum.
    xmin : int, optional
        Minimum wavenumber to plot. The default is 60.
    xmax : int, optional
        Maximum wavenumber to plot. The default is 700.

    Returns
    Figure
    """
    if len(files) > 1:
        for file, label in zip(files, labels):
            print('Plotting multiple spectra')
            data = pd.read_table(file, delimiter = '\t', header = 12)
            data.columns = ['Wavenumber', 'Intensity']
            # data['Intensity'] = np.interp(data['Intensity'], (data['Intensity'].min(), data['Intensity'].max()), (0, 1))
            plt.plot(data['Wavenumber'][:], data['Intensity'][:], label = label, linewidth = 0.5)
            plt.title('Raw Pristine Spectra')
            plt.legend()
            plt.xlabel('Wavenumber (cm$^{-1}$)')
            # plt.xlim(xmin, xmax)
            plt.ylabel('Intensity (CCD counts)')

    else:
        print('Plotting one spectra')
        data = pd.read_table(files[0], delimiter = '\t', header = 12)
        data.columns = ['Wavenumber', 'Intensity']
        # data['Intensity'] = np.interp(data['Intensity'], (data['Intensity'].min(), data['Intensity'].max()), (0, 1))
        plt.plot(data['Wavenumber'][:], data['Intensity'][:], label = labels, linewidth = 0.5)
        plt.title('Raw Spectra of Pristine ' + labels)
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        # plt.xlim(xmin, xmax)
        plt.ylabel('Intensity (CCD counts)')

        if save:
            plt.savefig(save_loc + '\\' + labels + '_raw.png')
            plt.close()
        else:
            plt.show()

def raw_raman_complex_plot(files, labels, save_loc, save=False):


        print('Plotting one spectra')
        data = pd.read_table(files[0], delimiter = '\t', header = 12, skiprows=20)
        data.columns = ['Wavenumber', 'Intensity']
        wavenumber, intensity = data['Wavenumber'], data['Intensity']
        plt.plot(data['Wavenumber'][:], data['Intensity'][:], label = labels, linewidth = 0.5)
        plt.title('Raw Spectra of Pristine ' + labels)
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        plt.ylabel('Intensity (CCD counts)')

        if save:
            plt.savefig(save_loc + '\\' + labels + '_raw.png')
            plt.close()
        else:
            plt.show()

        return data, wavenumber, intensity

def smooth_raman_and_peaks(wavenumber, intensity, labels, sigma=2, prominence=5, distance = 10):
    """
    Function to smooth Raman data and find peaks.
    Uses a Gaussian filter to smooth the data and then finds peaks using the find_peaks function from scipy.signal.
    
    Parameters:
    -----------
    wavenumber : array
        Wavenumber data.
    intensity : array
        Intensity data.
    labels : string
        Label for the plot.
    sigma : int, optional
        Sigma value for the Gaussian filter. The default is 2.
    prominence : int, optional
        Prominence value for the find_peaks function. The default is 5.
    distance : int, optional
        Distance value for the find_peaks function. The default is 10.
    
    Returns:
    --------
    roughpeaks : list
        List of rough peak locations.
    
    """
    # smooth data with gaussian filter
    sigma = sigma
    smoothed_intensity = gaussian_filter(intensity, sigma=sigma)
    print('Gaussian Smoothing Correctly Applied with Sigma = {}'.format(sigma))

    # find peaks and plot crosses at peak locations from smoothed data
    peaks_ix, _ = find_peaks(smoothed_intensity, prominence=prominence, distance=distance)
    # peaks_x, peaks_y = wavenumber[peaks_ix], smoothed_intensity[peaks_ix]
    wavenumber = wavenumber.reset_index(drop=True)
    peaks_x, peaks_y = wavenumber[peaks_ix], smoothed_intensity[peaks_ix]
    roughpeaks = peaks_x[:].tolist()
    print('Rough peak locations are: \n', roughpeaks, '\n Are you satisfied with these peaks?')

    # plot smoothed and raw data, and peaks
    plt.plot(wavenumber, smoothed_intensity, label = 'Gaussian Smoothing, $\sigma$ = {}'.format(sigma), linewidth = 2)
    plt.plot(wavenumber, intensity, label = labels, linewidth = 0.5)
    plt.plot(peaks_x, peaks_y, "x")
    plt.axhline(0, color='grey', linestyle='--')
    print('Plotting done')

    # annotate plot
    plt.title('Spectra of Pristine ' + labels)
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Intensity (CCD counts)')
    plt.legend()
    plt.show()

    return roughpeaks, smoothed_intensity

def plot_multiple(files, labels, sample, processed=False):
    for file, name in zip(files, labels):

        if processed:
            data = pd.read_csv(file)
            data.columns = ['Wavenumber', 'Intensity']
            wavenumber, intensity = data['Wavenumber'], data['Intensity']
            plt.plot(wavenumber, intensity, label = name)

            plt.xlim(125, 700)
            plt.title('Processed Raman Spectra of {}'.format(sample))
            plt.ylabel('Normalised Intensity (CCD counts)')

        else:
            data = pd.read_table(file, delimiter = '\t', header = 12, skiprows=20)
            data.columns = ['Wavenumber', 'Intensity']
            wavenumber, intensity = data['Wavenumber'], data['Intensity']
            plt.plot(wavenumber, intensity, linewidth=0.5, label = name)

            plt.title('Raw Raman Spectra of {}'.format(sample))
            plt.ylabel('Intensity (CCD counts)')

    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.legend()
    plt.show()

    return

### SCRIPT ###
label = 'Fu21Gd-SM1c'
file = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw data\Fu21Gd-SM1c-532nm.txt"]
save_loc = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Normalised Raw Spectra - Full Range"

# ~~~~~~~~~~~~~~~~~  Plot raw raman data as it is over full range ~~~~~~~~~~~~~~~~~~~~~~~ # 
data, wavenumber, intensity = raw_raman_complex_plot(file, label, save_loc=save_loc, save=False) # plot simple raw data

# ~~~~~~~~~~~~~~~~~ Processing data (bkg, normalsie) ~~~~~~~~~~~~~~~~~~~~~~~~  # 
wavenumber, intensity = filter_data(data, wavenumber, intensity, 66) # removing some low values to improve snip fit
wavenumber, sub_int = remove_background_snip(wavenumber, intensity, label) # remove background using snip

sigma = 2
smoothed_intensity = gaussian_filter(sub_int, sigma=sigma) # smooth data with gaussian filter
norm_int = normalise_intensity(smoothed_intensity) # normalise intensity

# ~~~~~~~~~~~~~~~~~  Plot smoothed data ~~~~~~~~~~~~~~~~~~ # 
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].plot(wavenumber, smoothed_intensity, linewidth=1, color = 'orange', label = 'Gaussian Smoothed ($\sigma$ = 2)')
axs[0].scatter(wavenumber, sub_int, s=1, color='blue', marker = 'x', label = 'Background Subtracted')
axs[0].set_title('Smoothed and Background Subtracted...')
axs[0].set_ylabel('Intensity (CCD counts)')
axs[0].set_xlabel('Wavenumber (cm$^{-1}$)')
axs[0].legend()

axs[1].plot(wavenumber, norm_int, linewidth = 0.5)
axs[1].set_title('...then Normalised')
axs[1].set_ylabel('Normalised Intensity')
axs[1].set_xlabel('Wavenumber (cm$^{-1}$)')

# Adjust layout to prevent overlap
plt.suptitle(label + ' Pristine')
plt.tight_layout()
plt.show()



# ~~~~~~~~~~~~~~~~~~~ Convert to dataframe ~~~~~~~~~~~~~~~~~~~~~ #
final_df = pd.DataFrame({
    'Wavenumber': wavenumber,
    'Intensity': norm_int
    })

final_df.reset_index(drop=True, inplace=True)
print(final_df.head()) # Print the first few rows of the DataFrame
final_df.to_csv('processed_spectra' + '\\' + label + '_processed.csv', index=False)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Plotting Multiple Raw Files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
labels = 'SM3a', 'SM3b', 'SM3c'
sample = 'Pristine SP11'

files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw data\Fu21Gd-SM1c-532nm.txt",
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw data\Fu21Gd-SM1a-532nm.txt",
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw data\Fu21Gd-SM1b-532nm.txt"]
# plot_multiple(files, labels, sample, processed=False) # raw

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Plotting Multiple Processed Files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
files = [r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_spectra\SP11-SM3a_processed.csv',
        r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_spectra\SP11-SM3b_processed.csv',
        r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_spectra\SP11-SM3c_processed.csv']
plot_multiple(files, labels, sample, processed=True) # processed 

##TODO: am I pre-processing too much? Dpo I need to smooth? I think yeah...


# ~~~~~~~~~~~~~ - Gaussian Smooth and find Peaks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
# roughpeaks, smoothed_intensity = smooth_raman_and_peaks(wavenumber, norm_int, label, sigma=2, prominence=0.05)


# no_peaks = len(roughpeaks)


# mod = LorentzianModel()
# pars = mod.guess(smoothed_intensity, x=wavenumber)
# pars['center'].set(value=roughpeaks[0], vary=True, expr='')
# out = mod.fit(smoothed_intensity, pars, x=wavenumber)

# plt.plot(wavenumber, smoothed_intensity, label = 'Smoothed Intensity', linewidth=0.5)
# plt.plot(wavenumber, out.best_fit, 'r-', label='Lorentzian fit')

# plt.xlabel('Wavenumber (cm$^{-1}$)')
# plt.ylabel('Normalised Intensity (CCD counts)')
# plt.legend()
# plt.show()


## TODO: edit this so first
# a - choose a range/ window to view the selected peaks over. Plot two vertical lines on full plot
# b - select number of peaks to fit and size of fitting window (probably peak position + - some width, to ensure range on either side of peak is sufficient)
# c - fit peaks with Lorentzian model and plot the fit on the selected range as an overlay to the full plot

# select 

# # select individual peak by roughpeak value
# window = 20
# peak_no = 8
# window_bot, window_top = int(roughpeaks[peak_no - 1 ] - window), int(roughpeaks[peak_no - 1] + window)
# print('Looking at Peak number {} at wavenumber {}'.format(peak_no, roughpeaks[peak_no -1]))

# int_for_peak = smoothed_intensity[window_bot:window_top]
# wavenumber_for_peak = wavenumber[window_bot:window_top]

# # Plotting figure to 
# plt.scatter(wavenumber, smoothed_intensity, label = 'Smoothed Intensity', s=1)
# plt.axvline(wavenumber_for_peak.iloc[0], color='b', linestyle='--')
# plt.axvline(wavenumber_for_peak.iloc[-1], color='b', linestyle='--')






# # plt.scatter(wavenumber_for_peak, int_for_peak, label = 'Peak {}'.format(peak_no), marker='x', color='r', s=5)

# # fitting individual peak...
# # mod = VoigtModel()
# # pars = mod.guess(int_for_peak, x=wavenumber_for_peak)
# # pars['gamma'].set(value=0.7, vary=True, expr='')
# # out = mod.fit(int_for_peak, pars, x=wavenumber_for_peak)
# # plt.plot(wavenumber_for_peak, out.best_fit, 'r-', label='Voigt fit')


# # mod = GaussianModel()
# # pars = mod.guess(int_for_peak, x=wavenumber_for_peak)
# # out = mod.fit(int_for_peak, pars, x=wavenumber_for_peak)
# # plt.plot(wavenumber_for_peak, out.best_fit, 'r-', label='Gaussian fit')

# # # mod = LorentzianModel()

# plt.xlabel('Wavenumber (cm$^{-1}$)')
# plt.ylabel('Normalised Intensity (CCD counts)')
# plt.legend()
# plt.show()






# # # Smoothing data using moving average
# # for i in range(1,30,5):
# #     window_size = i
# #     smoothed_intensity = intensity.rolling(window=window_size, center=True).mean()
# #     plt.plot(wavenumber, smoothed_intensity, label = 'Window Size {}'.format(i), linewidth = 0.5)

# # plt.xlabel('Wavenumber (cm$^{-1}$)')
# # plt.xlim(60, 700)
# # plt.ylabel('Intensity (CCD counts)')
# # plt.title('Fu21Gd Raman Spectra with Rolling Average Smoothing')
# # plt.legend() 
# # plt.show()

# ## TODO: try smoothing with different average and then normalising 
# ## TODO: try fitting peaks with lorentzian





# # """ MISCELLANEOUS PREVIOUS CODE 
# # label = 'SP11-SM3c'
# # file = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\SP11-SM3c-532nm.txt"]
# # save_loc = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Normalised Raw Spectra - Full Range"

# # # plotting function
# # # raw_raman_simple_plot(file, label, save_loc=save_loc, save=False)
# # # print('Step 1 finished: \n Raw data plotted over full range')

# # # ~~~~~~~~~~~~~~~~~ 2 - Plot normalised range over shorter range ~~~~~~~~~~~~~~~~~~~~~~~ #

# # label = 'SP11-SM3c'
# # file = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\SP11-SM3c-532nm.txt"]
# # save_loc = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Normalised Raw Spectra - Full Range"

# # # plotting function (note skips first 20 rows to drop Rayleigh peak)
# # # raw_raman_complex_plot(file, label, save_loc=save_loc, save=False)
# # # print('Step 2 finished: \n Rayleigh peak dropped.')
# # """