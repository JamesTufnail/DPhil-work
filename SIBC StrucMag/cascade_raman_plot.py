import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks



"""               RAMAN              """

labels = 'SM1a', 'SM1b', 'SM1c', 'SM2a', 'SM2b', 'SM2c', 'SM3a', 'SM3b', 'SM3c'

files = [
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\Fu21Gd-SM1a_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\Fu21Gd-SM1b_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\Fu21Gd-SM1c_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SuNAM21Gd-SM2a_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SuNAM21Gd-SM2b_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SuNAM21Gd-SM2c_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SP11-SM3a_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SP11-SM3b_processed.csv',
    r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_raman_spectra\SP11-SM3c_processed.csv'
]


offset = 0   
for file, name in zip(files, labels):

    data = pd.read_csv(file)
    angle, intensity = data['Wavenumber'], data['Intensity']
    # root_intensity = [i**0.5 for i in intensity]

    if 'Fu21Gd' in file:
        sample = 'Fu21Gd-'
    elif 'SuNAM21Gd' in file:
        sample = 'SuNAM21Gd-'
        intensity = [i+1 for i in intensity]
    elif 'SP11' in file:
        sample = 'SP11-'
        intensity = [i+2 for i in intensity]
    
    
    plt.plot(angle, intensity, linewidth=1, label = sample + name)

plt.ylabel('Normalised Intensity (a.u.)', fontsize='large')
plt.yticks([])
plt.xlabel('Wavenumber ($cm^{-1}$)', fontsize='large')
plt.title('Pristine Processed Raman Scans', fontsize='large')

# Get handles and labels, and reverse their order
handles, labels = plt.gca().get_legend_handles_labels()
handles.reverse()
labels.reverse()


# plt.legend(handles, labels, loc='upper left')#, bbox_to_anchor=(1, 1), fontsize='medium')
plt.xlim(50,700)

# add reference lines 
modes = [113.62, 145.656, 230.706, 262.84, 329.574, 451.851, 505.431, 594.564]
assignments = ['Ba', 'Cu(2)', 'd$_1$', '?', 'OII-OIII', 'OII+OIII', 'OIV', 'd$_2$']
shifts = [0, 0 , ]

# reflection = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '0010', '0011', '0012', '0013']


for mode, assignment in zip(modes, assignments):
    plt.axvline(x=mode, color='grey', linestyle='--', linewidth=0.5)
    # plt.text(mode, 3, assignment, fontsize='medium', 
            #  ha='center',  # Center the text horizontally
            #  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha = 0.5))

plt.show()


prominence = 0.02
distance = 10   

# for file in files:
#     data = pd.read_csv(file)

#     wavenumber, intensity = data['Wavenumber'], data['Intensity']

#     # find peaks and plot crosses at peak locations from smoothed data
#     peaks_ix, _ = find_peaks(intensity, prominence=prominence, distance=distance)
#     # peaks_x, peaks_y = wavenumber[peaks_ix], smoothed_intensity[peaks_ix]
#     wavenumber = wavenumber.reset_index(drop=True)
#     peaks_x, peaks_y = wavenumber[peaks_ix], intensity[peaks_ix]
#     roughpeaks = peaks_x[:].tolist()
#     print('File is \n', file, '\n Rough peak locations are: \n', roughpeaks)
