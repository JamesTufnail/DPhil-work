import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pandas import DataFrame

# choose raw or subtracted data
Subtracted = 'OFF'

# set variables
x_lim = 900
verticals = 'ON'
annotate_height = 6

# Inputting known values of pristine peaks taken from Thompsen and Kaczmaryzek
Ba_freq = 115
Cu2_freq = 154
O2_O3_freq1 = 334
O2_O3_freq2 = 438
O4_freq = 502

# reading data
if Subtracted == 'OFF':
    data_jt1_1_1 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                               r"Tufnail\JT1_1_1.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_jt1_1_2 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                               r"Tufnail\JT1_1_2.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_jt1_1_3 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                               r"Tufnail\JT1_1_3.txt", skiprows=38, delimiter='\t', encoding='cp1252')

    data_ss2_1 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS2_1.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_ss2_2 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS2_2.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_ss2_3 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS2_3.txt", skiprows=38, delimiter='\t', encoding='cp1252')

    data_ss6_1 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS6_1.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_ss6_2 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS6_2.txt", skiprows=38, delimiter='\t', encoding='cp1252')
    data_ss6_3 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                             r"Tufnail\SS6_3.txt", skiprows=43, delimiter='\t', encoding='cp1252')

else:
    data_jt1_1_1 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James "
                                 r"Tufnail\Begbroke_Raman_subtracted_data\JT111.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'])
    data_jt1_1_2 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\JT112.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)
    data_jt1_1_3 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\JT113.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)

    data_ss2_1 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS21.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)
    data_ss2_2 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS22.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)
    data_ss2_3 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS23.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)

    data_ss6_1 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS61.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)
    data_ss6_2 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS62.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)
    data_ss6_3 = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\Begbroke_Raman_subtracted_data\SS63.xlsx", usecols=['Subtracted_Data X1',
 'Subtracted_Data Y1'], skiprows=1)


print(data_ss6_3)

# Setting as dataframe
jt1_1_1_df = pd.DataFrame(data_jt1_1_1)
jt1_1_2_df = pd.DataFrame(data_jt1_1_2)
jt1_1_3_df = pd.DataFrame(data_jt1_1_3)
ss6_1_df = pd.DataFrame(data_ss6_1)
ss6_2_df = pd.DataFrame(data_ss6_2)
ss6_3_df = pd.DataFrame(data_ss6_3)
ss2_1_df = pd.DataFrame(data_ss2_1)
ss2_2_df = pd.DataFrame(data_ss2_2)
ss2_3_df = pd.DataFrame(data_ss2_3)

# Labelling columns
jt1_1_1_df.columns = ['Wavenumber', 'Counts']
jt1_1_2_df.columns = ['Wavenumber', 'Counts']
jt1_1_3_df.columns = ['Wavenumber', 'Counts']

ss2_1_df.columns = ['Wavenumber', 'Counts']
ss2_2_df.columns = ['Wavenumber', 'Counts']
ss2_3_df.columns = ['Wavenumber', 'Counts']

ss6_1_df.columns = ['Wavenumber', 'Counts']
ss6_2_df.columns = ['Wavenumber', 'Counts']
ss6_3_df.columns = ['Wavenumber', 'Counts']

# Normalising data
jt1_1_1_df['Counts'] = (jt1_1_1_df['Counts'] - jt1_1_1_df['Counts'].min()) / (
            jt1_1_1_df['Counts'].max() - jt1_1_1_df['Counts'].min())
jt1_1_2_df['Counts'] = (jt1_1_2_df['Counts'] - jt1_1_2_df['Counts'].min()) / (
            jt1_1_2_df['Counts'].max() - jt1_1_2_df['Counts'].min())
jt1_1_3_df['Counts'] = (jt1_1_3_df['Counts'] - jt1_1_3_df['Counts'].min()) / (
            jt1_1_3_df['Counts'].max() - jt1_1_3_df['Counts'].min())
ss2_1_df['Counts'] = (ss2_1_df['Counts'] - ss2_1_df['Counts'].min()) / (
            ss2_1_df['Counts'].max() - ss2_1_df['Counts'].min())
ss2_2_df['Counts'] = (ss2_2_df['Counts'] - ss2_2_df['Counts'].min()) / (
            ss2_2_df['Counts'].max() - ss2_2_df['Counts'].min())
ss2_3_df['Counts'] = (ss2_3_df['Counts'] - ss2_3_df['Counts'].min()) / (
            ss2_3_df['Counts'].max() - ss2_3_df['Counts'].min())
ss6_1_df['Counts'] = (ss6_1_df['Counts'] - ss6_1_df['Counts'].min()) / (
            ss6_1_df['Counts'].max() - ss6_1_df['Counts'].min())
ss6_2_df['Counts'] = (ss6_2_df['Counts'] - ss6_2_df['Counts'].min()) / (
            ss6_2_df['Counts'].max() - ss6_2_df['Counts'].min())
ss6_3_df['Counts'] = (ss6_3_df['Counts'] - ss6_3_df['Counts'].min()) / (
            ss6_3_df['Counts'].max() - ss6_3_df['Counts'].min())

# offsetting data
#jt1_1_1_df['Counts'] = jt1_1_1_df['Counts'] + 0.5
jt1_1_1_df['Counts'] = jt1_1_1_df['Counts'] + 0.5
jt1_1_3_df['Counts'] = jt1_1_3_df['Counts'] + 1.0
ss2_1_df['Counts'] = ss2_1_df['Counts'] + 1.5
ss2_2_df['Counts'] = ss2_2_df['Counts'] + 2.5
ss2_3_df['Counts'] = ss2_3_df['Counts'] + 3
ss6_1_df['Counts'] = ss6_1_df['Counts'] + 4
ss6_2_df['Counts'] = ss6_2_df['Counts'] + 4.5
ss6_3_df['Counts'] = ss6_3_df['Counts'] + 5

# plotting files

#gs = gridspec.GridSpec(2, 1)
#fig = plt.figure()
#fig, ax = plt.subplots(nrows=2, ncols=1)


# Light spectra plot
plt.plot(jt1_1_1_df['Wavenumber'], jt1_1_1_df['Counts'], linewidth=1, label='JT 1.1-1')
plt.plot(jt1_1_2_df['Wavenumber'], jt1_1_2_df['Counts'], linewidth=1, label='JT 1.1-2')
plt.plot(ss2_1_df['Wavenumber'], ss2_1_df['Counts'], linewidth=1, label='SS2-1')
plt.plot(ss2_3_df['Wavenumber'], ss2_3_df['Counts'], linewidth=1, label='SS2-3')
plt.plot(ss6_1_df['Wavenumber'], ss6_1_df['Counts'], linewidth=1, label='SS6-1')
plt.plot(ss6_3_df['Wavenumber'], ss6_3_df['Counts'], linewidth=1, label='SS6-3')

# dark spectra plot
plt.plot(jt1_1_3_df['Wavenumber'], jt1_1_3_df['Counts'], linewidth=1, ls='-.', label='JT 1.1-3')
plt.plot(ss2_2_df['Wavenumber'], ss2_2_df['Counts'], linewidth=1, ls='-.', label='SS2-2')
plt.plot(ss6_2_df['Wavenumber'], ss6_2_df['Counts'], linewidth=1, ls='-.', label='SS6-2')


# Plotting vertical lines through peaks
if verticals == 'ON':
    plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
    plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')

    plt.axvline(x=600,ls='--', lw='0.5', color='black')

    # Adding annotation arrows for known peaks
    plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('Cu(2)', xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 0.1),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

plt.title('Raman Spectroscopy of SP-11 CCs.')
plt.xlim(left=50, right=x_lim)
plt.xlabel('Rel. Wavenumber (cm$^{-1}$)')
plt.ylabel('Relative Intensity')
plt.legend(loc='upper right')
plt.show()
