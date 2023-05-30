# Script to read raman data and plot spectra

import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

# setting variables
verticals = 'ON'
labels = 'OFF'
annotate_height = 2400
# Inputting known values of pristine peaks
Ba_freq = 110
Cu2_freq = 145
O2_O3_freq1 = 332
O2_O3_freq2 = 438
O4_freq = 495


# reading curve fit exported from Origin
jt1_1_1 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\JT1.1-1.xlsx",
    sheet_name='nlfitpeaksCurve1')
jt1_1_2 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\JT1.1-2.xlsx",
    sheet_name='nlfitpeaksCurve1')
jt1_1_3 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\JT1.1-3.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS6_1 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS6-1.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS6_2 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS6-2.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS6_3 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS6-3.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS2_1 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS2-1.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS2_2 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS2-2.xlsx",
    sheet_name='nlfitpeaksCurve1')
SS2_3 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\SS2-3.xlsx",
    sheet_name='nlfitpeaksCurve1')

# converting to dataframe for easier manipulation
jt1_1_1df = pd.DataFrame(jt1_1_1, columns=['Independent Variable', 'Cumulative Fit Peak'])
jt1_1_2df = pd.DataFrame(jt1_1_2, columns=['Independent Variable', 'Cumulative Fit Peak'])
jt1_1_3df = pd.DataFrame(jt1_1_3, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS6_1df = pd.DataFrame(SS6_1, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS6_2df = pd.DataFrame(SS6_2, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS6_3df = pd.DataFrame(SS6_3, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS2_1df = pd.DataFrame(SS2_1, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS2_2df = pd.DataFrame(SS2_2, columns=['Independent Variable', 'Cumulative Fit Peak'])
SS2_3df = pd.DataFrame(SS2_3, columns=['Independent Variable', 'Cumulative Fit Peak'])

# offset 2nd and 3rd vertically in y
jt1_1_2df['Cumulative Fit Peak'] = 400 + jt1_1_2df['Cumulative Fit Peak']
jt1_1_3df['Cumulative Fit Peak'] = 800 + jt1_1_3df['Cumulative Fit Peak']
#SS6_1df['Cumulative Fit Peak'] = 1200 + SS6_1df['Cumulative Fit Peak']
#SS6_2df['Cumulative Fit Peak'] = 1600 + SS6_2df['Cumulative Fit Peak']
#SS6_3df['Cumulative Fit Peak'] = 2000 + SS6_3df['Cumulative Fit Peak']
SS2_1df['Cumulative Fit Peak'] = 1200 + SS2_1df['Cumulative Fit Peak']
SS2_2df['Cumulative Fit Peak'] = 1600 + SS2_2df['Cumulative Fit Peak']
SS2_3df['Cumulative Fit Peak'] = 2000 + SS2_3df['Cumulative Fit Peak']

# plotting RAMAN data on same figure
plt.plot(jt1_1_1df['Independent Variable'], jt1_1_1df['Cumulative Fit Peak'], label='Pristine SP11-1', linewidth=1.0)
plt.plot(jt1_1_2df['Independent Variable'], jt1_1_2df['Cumulative Fit Peak'], label='Pristine SP11-2', linewidth=1.0)
plt.plot(jt1_1_3df['Independent Variable'], jt1_1_3df['Cumulative Fit Peak'], label='Pristine SP11-3', linewidth=1.0)
#plt.plot(SS6_1df['Independent Variable'], SS6_1df['Cumulative Fit Peak'], label='SS6-1', linewidth=1.0, ls='--')
#plt.plot(SS6_2df['Independent Variable'], SS6_2df['Cumulative Fit Peak'], label='SS6-2', linewidth=1.0, ls='--')
#plt.plot(SS6_3df['Independent Variable'], SS6_3df['Cumulative Fit Peak'], label='SS6-3', linewidth=1.0, ls='--')
plt.plot(SS2_1df['Independent Variable'], SS2_1df['Cumulative Fit Peak'], label='Ion irradiated SP11-1', linewidth=1.0, ls='-.') #SS2-1
plt.plot(SS2_2df['Independent Variable'], SS2_2df['Cumulative Fit Peak'], label='Ion irradiated SP11-2', linewidth=1.0, ls='-.')
plt.plot(SS2_3df['Independent Variable'], SS2_3df['Cumulative Fit Peak'], label='Ion irradiated SP11-3', linewidth=1.0, ls='-.')

peak_values= pd.DataFrame(['Ba', 'Cu2', 'OII-OIII', 'OII-OIII', 'OIV'], [Ba_freq, Cu2_freq, O2_O3_freq1, O2_O3_freq2, O4_freq])
#print(peak_values)

# Plotting vertical lines through peaks
if verticals == 'ON':
    plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
    plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')

    # Adding annotation arrows for known peaks
if labels == 'ON':
    plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('Cu(2)' , xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 100),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height),
             arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

# Formatting plot
plt.title('Raman Spectroscopy of SP-11 CC Tapes.', fontsize=20)
plt.xlim(right=750)
plt.xlabel('Wavenumber (cm$^{-1}$)', fontsize=16)
plt.ylabel('Counts', fontsize=16)
plt.legend(loc='upper right', fontsize=12)
#plt.text('Note that SS2-3 and SS2-2 are missing a fit on the smallest peak. Overall the background is very noisey, particularly for the irradiated samples.',
 #       loc = 'lower right', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
plt.show()

print('Note that SS2-3 and SS2-2 are missing a fit on the smallest peak. Overall the background is very noisey, particularly for the irradiated samples.')