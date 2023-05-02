import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
from plotting_functions import *
from mawatari_functions import *
import glob

### Code snippet to plot multiple mawatari files in loop

mawatari_files = sorted(
    glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\Birmingham "
              r"data\OneDrive_2023-01-30\2023-01-20 Neutron Irradiation of Disk Samples - Lot 1 ("
              r"copy)\Fu21Gdo_1\Irr0\PPMS Data\22 12 07\Mawatari*.csv"))

selected_files = mawatari_files[:1]

for file in selected_files:
    field_moment_plot(file)





# Inputting known values of pristine peaks taken from Thompsen and Kaczmaryzek
Ba_freq = 115
Cu2_freq = 150
O2_O3_freq1 = 334
O2_O3_freq2 = 438
O4_freq = 502
annotate_height = 2.5

# Set up Metal ID file names to iterate plot loop through
# i = [
#     r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal "
#     r"identification\Metal_1",
#     r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal "
#     r"identification\Metal_1i",
#     r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal "
#     r"identification\Metal_2",
#     r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal "
#     r"identification\Metal_3",
#     r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal "
#     r"identification\Metal_4"]
#
# # plotting XRD data for unknown Metals
# for i in i:
#     plot_xrd(i)
#
#
# plt.legend(loc='upper right')
# plt.show()
