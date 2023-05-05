import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotting_functions import *
from mawatari_functions import *
import glob

# selected_files = mawatari_files[:]



### Code snippet to plot multiple mawatari files in loop
mawatari_files = sorted(
    glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\Birmingham "
              r"data\OneDrive_2023-01-30\2023-01-20 Neutron Irradiation of Disk Samples - Lot 1 ("
              r"copy)\Fu21Gdo_1\Irr0\PPMS Data\22 12 07\Mawatari*.csv"))
#field_moment_plot(mawatari_files)

indices, data_df = find_indices(mawatari_files[0])
print(indices)
enumerated = enumerate(indices)
print(enumerated)
multiple_raw_mawatari(data_df, indices)

# for file in mawatari_files:
#     file_index = find_indices(file)
#     print(file_index)

    # sliced_data = indexing_and_slicing(file)
    # print(sliced_data)
    #multiple_raw_mawatari(data_df)
    ## TODO: convert the units here before the loop below!
    #cols = sliced_data.columns.to_numpy()
    # print(enumerate(cols))
    # plt.plot(sliced_data[cols[1]], sliced_data[cols[2]])
    # plt.show()

    # for i in range(len(sliced_data.columns)-2):
    #     plt.plot(sliced_data.iloc[:, i+1], sliced_data.iloc[:, i+2])
    # plt.show()

    # for col in cols[1:]:
    #     plt.plot()
    #
    #
    # for col in cols[1:]:
    #     plt.plot(sliced_data[col], sliced_data[str(col+1)])
    #     plt.show()




## Code snippet to plot XRD datafiles for TA work
## TODO: edit glob so that the excel file Metal_Peak_List can be in the same folder but be ignored!!
metal_xrd_data = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal identification\Metal_*",
                 ))
mgo_xrd_data = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\2. MgO quantitative analysis\*"))

# plot_xrd(mgo_xrd_data)
# plot_xrd(metal_xrd_data)


# Inputting known values of pristine peaks taken from Thompsen and Kaczmaryzek
Ba_freq = 115
Cu2_freq = 150
O2_O3_freq1 = 334
O2_O3_freq2 = 438
O4_freq = 502
annotate_height = 2.5


