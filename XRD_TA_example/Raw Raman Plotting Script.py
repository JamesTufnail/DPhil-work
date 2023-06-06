import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from raman_functions import *
from mawatari_functions import *
from developing_functions import *
from misc_functions import *
import glob

## TODO: generalise these into their own functions

############ Code snippet to plot all individual raman files from folder ##########
individual__raw_raman = False
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


############ General code snippet to plot raw cascade raman files from folder ##########
raw_cascade_raman = True
if raw_cascade_raman:

    # name = 'RAW CASCADE - 810YBCO-2b-2MeV He'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\Figures"

    ## TODO: check naming is correct with actual samples (check letters and include dose)
    # name = 'RAW CASCADE - 810YBCO-2c-2MeV-He-annealed'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\Figures"

    ## TODO: how was this one irradiated?
    # name = 'RAW CASCADE - 810YBCO-3b-3c'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\Figures"

    ## TODO: are the letters correct? and irradiation?
    # name = 'RAW CASCADE - 810YBCO-3b-3c-annealed'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\Figures"

    name = 'RAW CASCADE - 810YBCO-1a-pristine'
    x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\* (X-Axis).txt"
    y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\* (Y-Axis).txt"
    save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\MRF Raman_Jonathan_8310YBCO-1a\Figures"

    # Defining plot title, save path and actually plotting cascade
    title = name
    save_path = save + "\{}.png".format(name)
    plot_raw_raman_cascade(x_axis, y_axis, 'ON', 'ON', title, save_path)




