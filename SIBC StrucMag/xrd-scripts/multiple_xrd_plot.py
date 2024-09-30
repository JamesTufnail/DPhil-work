import matplotlib.pyplot as plt
import pandas as pd
from pybaselines import Baseline, utils
from scipy.signal import find_peaks


# labels = 'SM1a', 'SM1b', 'SM1c'
# sample = 'Fu21Gd'
# files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\Fu21Gd-SM1a-gonio-v1.csv",
#         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\Fu21Gd-SM1b-gonio-v1.csv",
#         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\Fu21Gd-SM1c-gonio-v1.csv"]

# sample = 'SuNAM21Gd'
# labels = 'SM2a', 'SM2b', 'SM2c'
# files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\SuNAM21Gd-SM2a-gonio-v1.csv",
#         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\SuNAM21Gd-SM2b-gonio-v1.csv",
#         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\SuNAM21Gd-SM2c-gonio-v3.csv"]

sample = 'SP11'
labels = 'SM3a', 'SM3b', 'SM3c'
files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\sp11-sm3a-gonio-scan-v1.csv",
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\sp11-sm3b-gonio-scan-v1.csv",
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\Exported\sp11-sm3c-gonio-scan-v1.csv"]

for file, name in zip(files, labels):
    data = pd.read_csv(file, delimiter = ',', header=28)

    angle, intensity = data['Angle'], data['Intensity']
    root_intensity = [i**0.5 for i in intensity]

    plt.plot(angle, root_intensity, linewidth=0.5, label = name)
    plt.title('Raw c-axis goniometer scan of {}'.format(sample))
    plt.xlabel('2$\\theta$ (degrees)')
    plt.ylabel(r'$\sqrt{Intensity}$ $(\sqrt{cps})$')
    plt.legend()
plt.show()





# # using baseline fitter function from pybaselines to fit a snip baseline
# baseline_fitter = Baseline(x_data=angle)
# bkg, params = baseline_fitter.snip(root_intensity, max_half_window=50, decreasing=True, smooth_half_window=3)

# # plot the data
# plt.plot(angle, root_intensity, label = 'Raw Data')
# plt.plot(angle, bkg, '--', label='Baseline')

# # add labels and title
# plt.xlabel('2$\\theta$ (degrees)')
# plt.ylabel(r'$\sqrt{Intensity}$ $(\sqrt{cps})$')
# plt.title('C-axis goniometer scan of {}'.format(sample))
# plt.legend()
# plt.show()



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
# plt.plot(peaks_x, peaks_y, "x")
# plt.axhline(0, color='grey', linestyle='--')

# plt.xlabel('2$\\theta$ (degrees)')
# plt.ylabel(r'$\sqrt{Intensity}$ $\sqrt{cps}$')
# plt.title('C-axis goniometer scan of {} with baseline removed'.format(sample))

# plt.show()