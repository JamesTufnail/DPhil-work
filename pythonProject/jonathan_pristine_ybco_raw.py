import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

# set variables
#x_lim = 950
verticals = 'ON'
labels = 'ON'
annotate_height = 2.5

# Inputting known values of pristine peaks taken from Thompsen and Kaczmaryzek
Ba_freq = 115
Cu2_freq = 150
O2_O3_freq1 = 334
O2_O3_freq2 = 438
O4_freq = 502

# reading data
data_wavenumber_8310YBCO_1a_022 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\01 Training - James--Spectrum--022--Spec.Data 1 (X-Axis).txt")

data_counts_8310YBCO_1a_022 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF "
                                            r"Raman_Jonathan_8310YBCO-1a\01 Training - "
                                            r"James--Spectrum--022--Spec.Data 1 (Y-Axis).txt")

data_wavenumber_8310YBCO_1a_025 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman "
                                                r"Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\02 Training - "
                                                r"James--Spectrum--025--Spec.Data 1 (X-Axis).txt")
data_counts_8310YBCO_1a_025 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF "
                                            r"Raman_Jonathan_8310YBCO-1a\02 Training - "
                                            r"James--Spectrum--025--Spec.Data 1 (Y-Axis).txt")

data_wavenumber_8310YBCO_1a_064 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman "
                                                r"Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\04 Training - "
                                                r"James--Spectrum--064--Spec.Data 1 (CRR) (X-Axis).txt")
data_counts_8310YBCO_1a_064 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF "
                                            r"Raman_Jonathan_8310YBCO-1a\04 Training - "
                                            r"James--Spectrum--064--Spec.Data 1 (CRR) (Y-Axis).txt")

data_wavenumber_8310YBCO_1a_065 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman "
                                                r"Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\03 Training - "
                                                r"James--Spectrum--065--Spec.Data 1 (X-Axis).txt")
data_counts_8310YBCO_1a_065 = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF "
                                            r"Raman_Jonathan_8310YBCO-1a\03 Training - "
                                            r"James--Spectrum--065--Spec.Data 1 (Y-Axis).txt")

# Setting as dataframe, combining into one (concat appends column, axis=1 means to the right. axis=0 means underneath)
# and adding column names
data_wavenumber_8310YBCO_1a_022_df = pd.Dataframe = (data_wavenumber_8310YBCO_1a_022)
data_counts_8310YBCO_1a_022_df = pd.Dataframe = (data_counts_8310YBCO_1a_022)
data_8310YBCO_1a_022_df = pd.concat([data_wavenumber_8310YBCO_1a_022_df, data_counts_8310YBCO_1a_022_df], axis=1)
data_8310YBCO_1a_022_df.columns = ['Wavenumber', 'Counts']

data_wavenumber_8310YBCO_1a_025_df = pd.Dataframe = (data_wavenumber_8310YBCO_1a_025)
data_counts_8310YBCO_1a_025_df = pd.Dataframe = (data_counts_8310YBCO_1a_025)
data_8310YBCO_1a_025_df = pd.concat([data_wavenumber_8310YBCO_1a_025_df, data_counts_8310YBCO_1a_025_df], axis=1)
data_8310YBCO_1a_025_df.columns = ['Wavenumber', 'Counts']

data_wavenumber_8310YBCO_1a_064_df = pd.Dataframe = (data_wavenumber_8310YBCO_1a_064)
data_counts_8310YBCO_1a_064_df = pd.Dataframe = (data_counts_8310YBCO_1a_064)
data_8310YBCO_1a_064_df = pd.concat([data_wavenumber_8310YBCO_1a_064_df, data_counts_8310YBCO_1a_064_df], axis=1)
data_8310YBCO_1a_064_df.columns = ['Wavenumber', 'Counts']

data_wavenumber_8310YBCO_1a_065_df = pd.Dataframe = (data_wavenumber_8310YBCO_1a_065)
data_counts_8310YBCO_1a_065_df = pd.Dataframe = (data_counts_8310YBCO_1a_065)
data_8310YBCO_1a_065_df = pd.concat([data_wavenumber_8310YBCO_1a_065_df, data_counts_8310YBCO_1a_065_df], axis=1)
data_8310YBCO_1a_065_df.columns = ['Wavenumber', 'Counts']

# Normalising data
data_8310YBCO_1a_022_df['Counts'] = (data_8310YBCO_1a_022_df['Counts'] - data_8310YBCO_1a_022_df['Counts'].min()) / (data_8310YBCO_1a_022_df['Counts'].max() - data_8310YBCO_1a_022_df['Counts'].min())
data_8310YBCO_1a_025_df['Counts'] = (data_8310YBCO_1a_025_df['Counts'] - data_8310YBCO_1a_025_df['Counts'].min()) / (data_8310YBCO_1a_025_df['Counts'].max() - data_8310YBCO_1a_025_df['Counts'].min())
data_8310YBCO_1a_064_df['Counts'] = (data_8310YBCO_1a_064_df['Counts'] - data_8310YBCO_1a_064_df['Counts'].min()) / (data_8310YBCO_1a_064_df['Counts'].max() - data_8310YBCO_1a_064_df['Counts'].min())
data_8310YBCO_1a_065_df['Counts'] = (data_8310YBCO_1a_065_df['Counts'] - data_8310YBCO_1a_065_df['Counts'].min()) / (data_8310YBCO_1a_065_df['Counts'].max() - data_8310YBCO_1a_065_df['Counts'].min())


# offsetting for cascade
data_8310YBCO_1a_022_df['Counts'] = data_8310YBCO_1a_022_df['Counts'] + 0.5
data_8310YBCO_1a_025_df['Counts'] = data_8310YBCO_1a_025_df['Counts'] + 1.0
data_8310YBCO_1a_064_df['Counts'] = data_8310YBCO_1a_064_df['Counts'] + 1.5
#data_8310YBCO_1a_065_df['Counts'] = data_8310YBCO_1a_065_df['Counts'] + 1.5

# plotting files
plt.plot(data_8310YBCO_1a_064_df['Wavenumber'], data_8310YBCO_1a_064_df['Counts'], linewidth=1, label = 'REBCO Surface 1') # 8310YBCO-1a-64
plt.plot(data_8310YBCO_1a_025_df['Wavenumber'], data_8310YBCO_1a_025_df['Counts'], linewidth=1, label = 'REBCO Surface 2') # 8310YBCO-1a-25

plt.plot(data_8310YBCO_1a_022_df['Wavenumber'], data_8310YBCO_1a_022_df['Counts'], linewidth=1, label = 'Surface Artifact 1')# 8310YBCO-1a-22
plt.plot(data_8310YBCO_1a_065_df['Wavenumber'], data_8310YBCO_1a_065_df['Counts'], linewidth=1, label = 'Surface Artifact 2') # 8310YBCO-1a-65

# Plotting vertical lines through peaks
if verticals == 'ON':
    plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
    plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')



if labels == 'ON':
    # Adding annotation arrows for known peaks
    plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('Cu(2)' , xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 0.1),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

plt.title('Raman Spectroscopy of Pristine YBCO Thin Film', fontsize=20)
plt.xlim(left=0, right=1500)
plt.xlabel('Rel. Wavenumber (cm$^{-1}$)', fontsize=18)
plt.ylabel('Relative Intensity', fontsize=18)
plt.legend(loc='upper right', fontsize=16)
plt.show()


# plotting files

