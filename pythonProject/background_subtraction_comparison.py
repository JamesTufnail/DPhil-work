import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

# TODO: overlay raw subtracted data for each subtraction method on corresponding fitted plot
# TODO: replot it all normalised
# TODO: plot the difference between raw(?) or subtracted(?) data to show which subtraction method is most representative
#  of true data

# set variables
x_lim = 950
verticals = 'OFF'

# Inputting known values of pristine peaks
Ba_freq = 110
Cu2_freq = 145
O2_O3_freq1 = 332
O2_O3_freq2 = 438
O4_freq = 495
#peak_values= pd.DataFrame(['Ba', 'Cu2', 'OII-OIII', 'OII-OIII', 'OIV'], [Ba_freq, Cu2_freq, O2_O3_freq1, O2_O3_freq2, O4_freq])
#print(peak_values)

# reading curve fit exported from Origin
# all data from jt1.1-1
asymmetric_least_squares = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1asymmetricleastsquares.xlsx",
    sheet_name='nlfitpeaksCurve1')
point_spline8 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-8pointspline.xlsx",
    sheet_name='nlfitpeaksCurve1')
point_spline12 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-12pointspline.xlsx",
    sheet_name='nlfitpeaksCurve1')
point_spline_mod12 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-12pointsplinemod.xlsx",
    sheet_name='nlfitpeaksCurve1')
point_spline16 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-16pointspline.xlsx",
    sheet_name='nlfitpeaksCurve1')
# importing raw JT1.1-1
raw = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
                    r"Measurements\Background_subtraction_comparisons\JT1.1-1asymmetricleastsquares.xlsx",
                    usecols=[0, 1, 3], skiprows=[0])
raw_point_spline8 = pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-8pointspline.xlsx",
    usecols=[0, 1, 3], skiprows=[0])
raw_point_spline12= pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-12pointspline.xlsx",
    usecols=[0, 1, 3], skiprows=[0])
raw_point_spline_mod12= pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-12pointsplinemod.xlsx",
    usecols=[0, 1, 3], skiprows=[0])
raw_point_spline16= pd.read_excel(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN "
    r"Measurements\Background_subtraction_comparisons\JT1.1-1-16pointspline.xlsx",
    usecols=[0, 1, 3], skiprows=[0])


print(raw_point_spline8)


# converting to dataframe for easier manipulation
asymmetric_least_squares_df = pd.DataFrame(asymmetric_least_squares, columns=['Independent Variable', 'Cumulative Fit Peak'])
point_spline8_df = pd.DataFrame(point_spline8, columns=['Independent Variable', 'Cumulative Fit Peak'])
point_spline12_df = pd.DataFrame(point_spline12, columns=['Independent Variable', 'Cumulative Fit Peak'])
point_spline_mod12_df = pd.DataFrame(point_spline_mod12, columns=['Independent Variable', 'Cumulative Fit Peak'])
point_spline16_df = pd.DataFrame(point_spline16, columns=['Independent Variable', 'Cumulative Fit Peak'])

# setting up difference vectors as zeros
#asymmetric_least_squares_diff_df = asymmetric_least_squares_df[['Independent Variable', 'Cumulative Fit Peak']].copy()

# calculating difference plot (i.e. raw data - subtracted fitted data = data missed in subtraction
#asymmetric_least_squares_diff_df['Cumulative Fit Peak'] = raw['Unnamed: 1'] - asymmetric_least_squares_diff_df['Cumulative Fit Peak']
#print(asymmetric_least_squares_diff_df)

# offset 2nd and 3rd vertically in y
point_spline8_df['Cumulative Fit Peak'] = 400 + point_spline8_df['Cumulative Fit Peak']
point_spline12_df['Cumulative Fit Peak'] = 800 + point_spline12_df['Cumulative Fit Peak']
point_spline_mod12_df['Cumulative Fit Peak'] = 1200 + point_spline_mod12_df['Cumulative Fit Peak']
point_spline16_df['Cumulative Fit Peak'] = 1600 + point_spline16_df['Cumulative Fit Peak']
raw['Unnamed: 1'] = 1600 + raw['Unnamed: 1']
raw_point_spline8['Subtracted from B'] = 400 + raw_point_spline8['Subtracted from B']
raw_point_spline12['Subtracted from B'] = 800 + raw_point_spline12['Subtracted from B']
raw_point_spline_mod12['Subtracted from B'] = 1200 + raw_point_spline_mod12['Subtracted from B']
raw_point_spline16['Unnamed: 3'] = 1600 + raw_point_spline16['Unnamed: 3']


# plotting RAMAN data on same figure
plt.plot(asymmetric_least_squares_df['Independent Variable'], asymmetric_least_squares_df['Cumulative Fit Peak'], label='Asymmetric Least Squares (ALS)', linewidth=1.0)
plt.plot(raw['Unnamed: 0'], raw['Subtracted from B'], label='ALS Subtracted Data', linewidth=1.0)
plt.plot(point_spline8_df['Independent Variable'], point_spline8_df['Cumulative Fit Peak'], label='8 Point Spline', linewidth=1.0)
plt.plot(point_spline12_df['Independent Variable'], point_spline12_df['Cumulative Fit Peak'], label='12 Point Spline', linewidth=1.0)
plt.plot(point_spline_mod12_df['Independent Variable'], point_spline_mod12_df['Cumulative Fit Peak'], label='12 Point Spline Mod', linewidth=1.0)
plt.plot(point_spline16_df['Independent Variable'], point_spline16_df['Cumulative Fit Peak'], label='16 Point Spline', linewidth=1.0)
plt.plot(raw['Unnamed: 0'], raw['Unnamed: 1'], label='Raw Data', linewidth=1.0)
plt.plot(raw_point_spline8['Unnamed: 0'], raw_point_spline8['Subtracted from B'], label = 'Raw Spline 8')
plt.plot(raw_point_spline12['Unnamed: 0'], raw_point_spline12['Subtracted from B'], label = 'Raw Spline 12')
plt.plot(raw_point_spline_mod12['Unnamed: 0'], raw_point_spline_mod12['Subtracted from B'], label = 'Raw Spline Mod 12')
plt.plot(raw_point_spline16['Unnamed: 0'], raw_point_spline16['Unnamed: 3'], label = 'Raw Spline 16')


# plotting difference
#plt.plot(asymmetric_least_squares_diff_df['Independent Variable'], asymmetric_least_squares_diff_df['Cumulative Fit Peak'], ls ='-', color = 'black')

# Plotting vertical lines through peaks
annotate_height = 3600
if verticals == 'ON':
    plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
    plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
    plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')

    # Adding annotation arrows for known peaks
    plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('Cu2', xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('OII-OIII', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 100),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('OII-OIII', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
    plt.annotate('OIV', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height),
                 arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

# Formatting plot
plt.title('Comparison of Background Subtraction Regimes.')
plt.xlim(right = x_lim)
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Counts')
plt.legend(loc='upper right')
plt.show()
