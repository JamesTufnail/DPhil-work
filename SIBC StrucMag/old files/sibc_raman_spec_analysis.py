## Raman spectroscopy analysis for for SIBC StrucMag experiment


import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import pandas as pd
from scipy.signal import savgol_filter
import sklearn.linear_model as lm
from sklearn.preprocessing import PolynomialFeatures
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from lmfit.models import LorentzianModel, VoigtModel, GaussianModel



# files = glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\*SuNAM21Gd-SM*.txt")

# files = (r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\1 SP11-SM3a-532nm.txt",
#          r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\3 SP11-SM3b-532nm.txt",
#          r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\4 SP11-SM3c-532nm.txt")

# labels = ('1a', '1b', '1c')



# files = (r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\1 SuNAM21Gd-SM2a-532nm.txt",
#           r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\3 SuNAM21Gd-2b-532nm avg.txt",
#          r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\4 SuNAM21Gd-SM2c-532nm avg.txt")

# labels = ('2a', '2b', '2c')

# files = (r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\1 Average of 5 Spectra.txt",
#         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\3 Fu21Gd-SM1b-532nm.txt",
#          r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine Raman Data\Pristine raw _ new (lower power)\4 Fu21Gd-SM1c-532nm.txt")

# labels = ('3a', '3b', '3c')


############### Functions ################

def plot_raman(files, labels, xmin=60, xmax=700):
    if len(files) > 1:
        for file, label in zip(files, labels):
            data = pd.read_table(file, delimiter = '\t', header = 12)
            data.columns = ['Wavenumber', 'Intensity']
            data['Intensity'] = np.interp(data['Intensity'], (data['Intensity'].min(), data['Intensity'].max()), (0, 1))
            plt.plot(data['Wavenumber'][100:], data['Intensity'][100:], label = label, linewidth = 0.5)
    else:
        print(files)
        data = pd.read_table(files, delimiter = '\t', header = 12)
        data.columns = ['Wavenumber', 'Intensity']
        data['Intensity'] = np.interp(data['Intensity'], (data['Intensity'].min(), data['Intensity'].max()), (0, 1))
        plt.plot(data['Wavenumber'][100:], data['Intensity'][100:], label = labels, linewidth = 0.5)

    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.xlim(xmin, xmax)
    plt.ylabel('Intensity (CCD counts)')
    plt.title('Average Pristine Raman Spectra')
    plt.legend()
    plt.show()

########  Script ###






"""# find rough peak

# gaussian smoothing
sigma = 2
smoothed_intensity = gaussian_filter(intensity, sigma=sigma)
plt.plot(wavenumber, smoothed_intensity, label = 'Sigma = {}'.format(sigma), linewidth = 0.5)
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Intensity (CCD counts)')

# peaks find for gaussian smoothed
prominence = 0.02
peaks_ix, _ = find_peaks(smoothed_intensity, prominence=prominence)
peaks_x, peaks_y = wavenumber[peaks_ix], smoothed_intensity[peaks_ix]
plt.plot(peaks_x, peaks_y, "x")

roughpeaks = peaks_ix[:].tolist()

print('Rough peak locations are: \n', roughpeaks, '\n Are you satisfied with these peaks?')
plt.show()

Fit individual peaks extracted from rough peaks
# select individual peak by roughpeak value
window = 40
peak_no = 8
intensity_peak = intensity[roughpeaks[peak_no]-window:roughpeaks[peak_no]+window]
wavenumber_peak = wavenumber[roughpeaks[peak_no]-window:roughpeaks[peak_no]+window]

# converting to dataframe
intensity_df, wavenumber_df = pd.DataFrame(intensity_peak, columns=['Intensity']), pd.DataFrame(wavenumber_peak, columns=['Wavenumber'])
intensity_df, wavenumber_df = intensity_df.reset_index(), wavenumber_df.reset_index()

plt.plot(wavenumber_peak, intensity_peak, label = 'Peak {}'.format(peak_no), linewidth = 0.5)


# fitting individual peak...
mod = VoigtModel()
# mod = GaussianModel()
mod = LorentzianModel()

pars = mod.guess(intensity_df['Intensity'], x=wavenumber_df['Wavenumber'])
pars['gamma'].set(value=0.7, vary=True, expr='')
out = mod.fit(intensity_df['Intensity'], pars, x=wavenumber_df['Wavenumber'])

plt.plot(wavenumber_df['Wavenumber'], out.best_fit, 'r-', label='Voigt fit')
plt.legend()
plt.show()
"""



""" Tryng a scipy get peaks function

peaks_ix, _ = find_peaks(intensity, prominence=0.075)
peaks_x, peaks_y = wavenumber[peaks_ix], intensity[peaks_ix]
plt.plot(peaks_x, peaks_y, "x")
plt.title('Raman Spectra with Peaks')
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Normalised Intensity (CCD counts)')
# plt.text()
# plt.show()
"""



"""
# Smoothing data using gaussian filter

for i in range(1, 6):
    smoothed_intensity = gaussian_filter(intensity, sigma=i)
    plt.plot(wavenumber, smoothed_intensity, label = 'Sigma {}'.format(i), linewidth = 0.5)
    
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.xlim(60, 700)
plt.ylabel('Intensity (CCD counts)')
plt.title('Fu21Gd Raman Spectra with Gaussian Smoothing')
plt.legend()
plt.show()
# plt.savefig('Fu21Gd_Raman_Gaussian_Smoothing.png')
"""



"""
# Smoothing data using moving average
for i in range(1,10,2):
    window_size = i
    smoothed_intensity = intensity.rolling(window=window_size, center=True).mean()
    plt.plot(wavenumber, smoothed_intensity, label = 'Window Size {}'.format(i), linewidth = 0.5)

plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.xlim(60, 700)
plt.ylabel('Intensity (CCD counts)')
plt.title('Fu21Gd Raman Spectra with Rolling Average Smoothing')
plt.legend() 
plt.show()
# plt.savefig('Fu21Gd_Raman_Rolling_Average.png')
"""


"""
# savitzky-golay filter smoothing
for i in range(1, 5):
    window_size = 15
    order = i
    smoothed_intensity = savgol_filter(intensity, window_size, order)
    plt.plot(wavenumber, smoothed_intensity, label = 'Polynomial Order {}'.format(order), linewidth = 0.5)

plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.xlim(60, 700)
plt.ylabel('Intensity (CCD counts)')
plt.title('Fu21Gd Raman Spectra with Savitzky-Golay Smoothing and Window Size {}'.format(window_size))
plt.legend() 
# plt.show()

plt.savefig('Fu21Gd_Raman_Savitzky-Golay window size {}.png'.format(window_size))
"""




"""
# Trying polynomial regression to fit data
# This is a terrible fit but maybe better if you isolate the peaks first...

for degree in range(1, 10):
    x_trans = PolynomialFeatures(degree=degree)  
    x_trans = x_trans.fit_transform(wavenumber.values.reshape(-1, 1))  
    
    lin_reg = lm.LinearRegression()  
    lin_reg.fit(x_trans, intensity)

    y_pred = lin_reg.predict(x_trans)
    plt.plot(wavenumber, y_pred, label = 'Polynomial Degree {}'.format(degree), linewidth = 0.5)

plt.xlabel('Wavenumber (cm$^{-1}$)')
# plt.xlim(60, 700)
plt.ylabel('')
plt.title('Fu21Gd Raman Spectra with Polynomial Regression')
plt.legend()
# plt.show()
# plt.savefig('Fu21Gd_Raman_Polynomial_Regression.png')
"""


