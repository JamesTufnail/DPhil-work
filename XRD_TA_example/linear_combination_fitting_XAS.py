import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from raman_functions import *

# File currently reads in datavalues from txt file, normalises y values and then plots
## TODO: write into a function...

# def normalise_and_plot_XANES():
# datasets = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots\Fu21Y*10deg.txt"))

Fu21 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked.nor",
                   delim_whitespace=' ', skiprows=14)
diff_Fu21 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked_diff_plots.nor",
                   delim_whitespace=' ', skiprows=14)

energy = Fu21.iloc[:, 0]

pristine_10deg = Fu21.iloc[:, 1].astype(float)
pristine_45deg = Fu21.iloc[:, 2].astype(float)
pristine_80deg = Fu21.iloc[:, 3].astype(float)

two_MeVO_10deg = Fu21.iloc[:, 4].astype(float)
two_MeVO_80deg = Fu21.iloc[:, 5].astype(float)

two_MeVO_ann_10deg = Fu21.iloc[:, 6].astype(float)
two_MeVO_ann_80deg = Fu21.iloc[:, 7].astype(float)

# plt.plot(energy, pristine_10deg, label='10 Degrees')
# plt.plot(energy, pristine_45deg, label='45 Degrees')
# plt.plot(energy, pristine_80deg, label='80 Degrees')

# plt.plot(energy, pristine_10deg, label='Pristine')
# plt.plot(energy, two_MeVO_10deg, label='2 MeV O$^+$')
# plt.plot(energy, two_MeVO_ann_10deg, label='Annealed')

plt.plot(energy, pristine_80deg, label='Pristine')
plt.plot(energy, two_MeVO_80deg, label='2 MeV O$^+$')
plt.plot(energy, two_MeVO_ann_80deg, label='Annealed')

# energy_diff = diff_Fu21.iloc[:, 0]
#
# ann_10deg_sub_p_10deg = diff_Fu21.iloc[:,1]
# _10deg_sub_p_10deg = diff_Fu21.iloc[:,2]
#
# ann_80deg_sub_p_80deg = diff_Fu21.iloc[:,3]
# _80deg_sub_p_80deg = diff_Fu21.iloc[:,4]

# plt.plot(energy_diff, ann_10deg_sub_p_10deg, label='Annealed')
# plt.plot(energy_diff, _10deg_sub_p_10deg, label='2 MeV O$^+$')
#
# plt.plot(energy_diff, ann_80deg_sub_p_80deg, label='Annealed')
# plt.plot(energy_diff, _80deg_sub_p_80deg, label='2 MeV O$^+$')

title = 'XANES Diff Spectra for Fu21 Tapes at 80 Degrees Beam Angle - reduced'

#plt.axhline(y=0, linestyle='--', color='black')
plt.legend()
plt.title(title)
plt.xlim(8975, 9015)
plt.xlabel('Energy (eV)')
plt.ylabel('Intensity')
# plt.show()
save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised" + '\\' + title
plt.savefig(save_path)
plt.close()

#
# labels = ['Pristine', '2 MeV O', 'Ann']
# title = 'XANES Spectra for Fu21 Tapes at 10 Degrees'

#
# normalised = []
#
# for i, file in enumerate(datasets):
#     data = pd.read_table(r"{}".format(file))
#     data_x = data.iloc[158:524].apply(lambda x: x.str.lstrip('-')).astype(float)
#     data_y = data.iloc[538:905].apply(lambda x: x.str.lstrip('-')).astype(float)
#     norm_y = normalising_to_tail(data_y)
#
#     normalised.append(norm_y)
#     plt.plot(data_x, norm_y, label = labels[i])
#
# plt.axhline(y=0, linestyle='--', color='black')
# plt.legend()
# plt.title(title)
# plt.xlim(8975, 9015)
# plt.xlabel('Energy (eV)')
# plt.ylabel('Intensity')
# plt.savefig(save_path)




#     #
# pristine_10deg_all = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21Y_p_10deg.txt")
# pristine_45deg_all = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21Y_p_45deg.txt")
# pristine_80deg_all = pd.read_table(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21Y_p_80deg.txt")
#
# pristine_10deg_x = pristine_10deg_all.iloc[158:524].apply(lambda x: x.str.lstrip('-')).astype(float)
# pristine_10deg_y = pristine_10deg_all.iloc[538:905].apply(lambda x: x.str.lstrip('-')).astype(float)
# norm_p_10deg_y = normalising_to_tail(pristine_10deg_y)
#
# pristine_45deg_y = pristine_45deg_all.iloc[538:905].apply(lambda x: x.str.lstrip('-')).astype(float)
# norm_p_45deg_y = normalising_to_tail(pristine_45deg_y)
#
# pristine_80deg_y = pristine_80deg_all.iloc[538:905].apply(lambda x: x.str.lstrip('-')).astype(float)
# norm_p_80deg_y = normalising_to_tail(pristine_80deg_y)
#
# plt.plot(pristine_10deg_x, norm_p_10deg_y, label='10 Degrees')
# plt.plot(pristine_10deg_x, norm_p_45deg_y, label='45 Degrees')
# plt.plot(pristine_10deg_x, norm_p_80deg_y, label='80 Degrees')
#
# title = 'XANES Spectra for pristine Fu21 Tapes at Different Beam Angles'
# plt.legend()
# plt.title(title)
# plt.xlim(8975, 9100)
# plt.xlabel('Energy (eV)')
# plt.ylabel('Intensity')
# #plt.show()
#
# save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots" + '\\' + title
# plt.savefig(save_path)

###############################################################
#
# x_labels = ['Pristine', '2 MeV O', 'Annealed']
# eighty_degree = [0.474, 0.458, 0.523]
# ten_degree = [0.526, 0.542, 0.477]
#
# plt.plot(x_labels, eighty_degree, label='80 Degree')
# plt.plot(x_labels, ten_degree, label='10 Degree')
#
# # Add data labels for the '80 Degree' line
# for i, j in zip(x_labels, eighty_degree):
#     plt.text(i, j, str(j), ha='center', va='bottom')
#
# # Add data labels for the '10 Degree' line
# for i, j in zip(x_labels, ten_degree):
#     plt.text(i, j, str(j), ha='center', va='top')
