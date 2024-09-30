import matplotlib.pyplot as plt
import pandas as pd



# labels = 'SM1a', 'SM1b', 'SM1c', 'SM2a', 'SM2b', 'SM2c', 'SM3a', 'SM3b', 'SM3c'

# files = [r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\Fu21Gd-SM1a_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\Fu21Gd-SM1b_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\Fu21Gd-SM1c_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SuNAM21Gd-SM2a_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SuNAM21Gd-SM2b_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SuNAM21Gd-SM2c_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SP11-SM3a_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SP11-SM3b_processed.csv',
# r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SP11-SM3c_processed.csv']

labels = '', '', 'SM3a='

files = [r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\Fu21Gd-SM1a_processed.csv',
r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SuNAM21Gd-SM2a_processed.csv',
r'C:\Users\James\PycharmProjects\SIBC StrucMag\processed_XRD_spectra\SP11-SM3a_processed.csv']

offset = 0   
for file, name in zip(files, labels):

    data = pd.read_csv(file)
    angle, intensity = data['Angle'], data['Intensity']
    # root_intensity = [i**0.5 for i in intensity]

    if 'Fu21Gd' in file:
        sample = 'Fu21Gd-'
        intensity = [i+offset for i in intensity]
        offset+=0.25
    elif 'SuNAM21Gd' in file:
        sample = 'SuNAM21Gd-'
        intensity = [i+0.5 for i in intensity]
        intensity = [i+offset for i in intensity]
        offset+=0.25
    elif 'SP11' in file:
        sample = 'SP11-'
        intensity = [i+1 for i in intensity]
        intensity = [i+offset for i in intensity]
        offset+=0.25
    
    
    plt.plot(angle, intensity, linewidth=1, label = sample + name)

plt.ylabel('$\sqrt{Intensity}$ (a.u.)', fontsize='large')
plt.yticks([])
plt.xlabel('2$\Theta$ (degrees)', fontsize='large')
plt.title('Pristine Gonio C-axis Scans', fontsize='large')

# Get handles and labels, and reverse their order
handles, labels = plt.gca().get_legend_handles_labels()
handles.reverse()
labels.reverse()

# Create the legend with the reversed order
# plt.legend(handles, labels, loc='upper left')#, bbox_to_anchor=(1, 1), fontsize='medium')

# add reference lines 
# x = [7.56, 15.16, 22.8, 30.6, 38.5, 46.65, 55.0, 63.7, 72.87, 82.56, 93.08, 104.7, 118] # based on YBCO 39359
x = [7.55, 15.13, 22.78, 30.5, 38.5, 46.5, 54.88, 63.56, 72.67, 82.35, 92.81, 104.38, 117.71]  # based on GdBCO 65393
reflection = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '0010', '0011', '0012', '0013']

k=0.1
for i, j in zip(x, reflection):
    plt.axvline(x=i, color='grey', linestyle='--', linewidth=0.5)
    plt.text(i-4, 2.2 + k, j, fontsize='medium', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
    k*=-1

plt.show()