import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from raman_functions import *
from mawatari_functions import *
from developing_functions import *
from misc_functions import *
import glob

## TODO: Plot all raw raman files and compare different samples with same parameters. Then plot same parameters but different samples together on cascade plot
## TODO: use a background subtraction and replot them all


############ Code snippet to plot individual raman files ##########
individual__raw_raman = True
if individual__raw_raman:

    # Raw 810YBCO-2b-2MeV-He
    # name = 'RAW - 810YBCO-2b-2MeV He'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\Figures"

    # Raw 810YBCO-2c-2MeV-He-annealed
    ## TODO: check naming is correct with actual samples (check letters and include dose)
    # name = 'RAW - 810YBCO-2c-2MeV-He-annealed'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\Figures"

    # Raw_810YBCO_3b_3c:
    ## TODO: how was this one irradiated?
    # name = 'RAW - 810YBCO-3b-3c'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\Figures"

    # Raw_810YBCO_3b_3c_annealed:
    ## TODO: are the letters correct? and irradiation?
    name = 'RAW - 810YBCO-3b-3c-annealed'
    x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (X-Axis).txt"))
    y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (Y-Axis).txt"))
    save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\Figures"

    # zipping together the x_axis and y_axis arrays and defining the loop variable of each x and y as x_file and y_file
    for x_file, y_file in zip(x_axis, y_axis):

        # Reading file name and determining save folder and name
        title = name + " __RAW__ {}".format(x_file[-48:-26])
        save_path = save + "\{}.png".format(name + " __ {}".format(x_file[-48:-26]))

        # Actual plotting function
        plot_raman_separate_files(x_file, y_file, 'ON', 'ON', title, save_path)


############ Code snippet to plot raw cascade raman files ##########
raw_cascade_raman = False
if raw_cascade_raman:
    x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (X-Axis).txt"
    y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (Y-Axis).txt"

    plot_raw_raman_cascade(x_axis, y_axis, 'ON', 'ON')



######### Code snippet to plot Susceptibility - Temperature plot
susceptibility = False
if susceptibility:
    indices, data_df = find_field_start(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron "
                                             r"Irradiation\Birmingham "
                                             r"data\data-for-manipulation-pristine-measurements\Fu21Gdo_1\Irr0\PPMS "
                                             r"Data\22 12 07\Susceptibility_Measurements.dat")
    print(data_df.head())
    print(data_df.tail())
    print(indices)
    magnetisation_measurements(data_df, indices)




########### Code snippet to plot multiple Mawatari files in loop #############
mawatari = False
if mawatari:
    mawatari_files = sorted(
        glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\Birmingham "
                  r"data\OneDrive_2023-01-30\2023-01-20 Neutron Irradiation of Disk Samples - Lot 1 ("
                  r"copy)\Fu21Gdo_1\Irr0\PPMS Data\22 12 07\Mawatari*.csv"))
    for file_no, file in enumerate(mawatari_files):
        indices, data_df = find_ramp_start(mawatari_files[file_no])
        title = find_title_from_filename(mawatari_files[file_no], '_', 1, -4)
        multiple_raw_mawatari(data_df, indices, title)
        #final_raw_mawatari(data_df, indices, file_no)
    print(indices)


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


