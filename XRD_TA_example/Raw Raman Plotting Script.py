
from raman_functions import *
import glob


""" README --- SCRIPT DESCRIPTION ---
This script will take the data from MRF raman txt files (x-axis) and (y-axis) and plot them into either individual 
plots, or into a larger cascade and save them in a folder in the sample folder called Figures.

You have to comment in the sections that are for the sample you want to plot. It will plot all the x-axis and y-axis
values in that folder, so you can move them out if you don't want them plotted.

THIS IS TO HELP INFORM YOUR DATA PROCESSING, NOT FOR DATA PRESENTATION DIRECTLY!!!
"""

### Code snippet to zip together selected Raman files
zipping_selected_files = False
if zipping_selected_files:
    x_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(X-Axis).txt"))
    y_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(Y-Axis).txt"))
    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Zipped Files for Origin"

    for x_file, y_file in zip(x_axis, y_axis):
        raman_zipping(x_file, y_file, save_path)

############ Code snippet to plot all individual raman files from folder ##########
## TODO: generalise these into their own functions
## TODO: check naming is correct with actual samples
individual__raw_raman = True
if individual__raw_raman:

    # name = 'RAW - 810YBCO-2b-2MeV He 3.6e16'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\Figures"

    # name = 'RAW - 810YBCO-2c-2MeV He 3.6e16 annealed'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\Figures"

    # name = 'RAW - 810YBCO-3b-3c 2MeV O 5e14'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\Figures"

    # name = 'RAW - 810YBCO-3b-3c 2MeV O 5e14 annealed'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\* (Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c-annealed\Figures"
    #
    # name = 'RAW - 810YBCO-1c-2c 8.6e15 300keV He'
    # x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He\*(X-Axis).txt"))
    # y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He\*(Y-Axis).txt"))
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He\Figures"

    name = 'RAW - 810YBCO-1c-2c 8.6e15 300keV He annealed'
    x_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He-annealed\*(X-Axis).txt"))
    y_axis = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He-annealed\*(Y-Axis).txt"))
    save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\810ybco-1c-2c-8.6e15-300keV-He-annealed\Figures"

    # zipping together the x_axis and y_axis arrays and defining the loop variable of each x and y as x_file and y_file
    for x_file, y_file in zip(x_axis, y_axis):

        # Reading file name and determining save folder and name
        title = name + " __RAW__ {}".format(x_file[-48:-26])
        save_path = save + "\{}.png".format(name + " __ {}".format(x_file[-48:-26]))

        # Actual plotting function
        plot_raman_separate_files(x_file, y_file, title, save_path)


############ General code snippet to plot raw cascade raman files from folder ##########
## TODO: generalise these into their own functions
raw_cascade_raman = False
if raw_cascade_raman:

    # name = 'RAW CASCADE - 810YBCO-2b-2MeV He 3.6e16'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2b-2MeV-He\Figures"

    ## TODO: check naming is correct with actual samples (check letters)
    # name = 'RAW CASCADE - 810YBCO-2c-2MeV-He 3.6e16 annealed'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-2c-2MeV-He-annealed\Figures"

    # name = 'RAW CASCADE - 810YBCO-3b-3c 2MeV O 5e14'
    # x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (X-Axis).txt"
    # y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\* (Y-Axis).txt"
    # save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\James Tufnail - YBCO thin films\810ybco-3b-3c\Figures"

    # name = 'RAW CASCADE - 810YBCO-3b-3c O 2MeV 5e14 annealed'
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
    plot_raw_raman_cascade(x_axis, y_axis, title, save_path)




