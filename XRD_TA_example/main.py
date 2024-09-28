from raman_functions import *
import pandas as pd
from PycharmProjects.mawatari_practice.mawatari_functions import *
from developing_functions import *
from misc_functions import *
import glob
from BaselineRemoval import BaselineRemoval

## TODO: Plot all raw raman files and compare different samples with same parameters. Then plot same parameters but different samples together on cascade plot
## TODO: use a background subtraction and replot them all


######################### Code snippet to plot selected RAW raman plots on same figure #####################
raw_selected_cascade = False
if raw_selected_cascade:
    ## TODO: Turn this into a function
    ### Make these the inputs to the function, you also need a function that will tell you the order so that yoy can choose the labelling
    x_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(X-Axis).txt"))
    y_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(Y-Axis).txt"))
    #print(y_axis) # Currently using to find file names and therefore determine what to set as labels
    ## TODO: write a function that actually finds the right names and generates a list of labels itself


    # save_name = '22light_raw_cascade' #Initial cascade, not including 300kev He
    # labels=['2b (3.6e16 2 MeV He$^+$ annealed)',
    #         '3b-3c (5e14 2 MeV O$^+$)',
    #         '2b (3.6e16 2 MeV He$^+$)',
    #         '2b (3.6e16 2 MeV He$^+$)',
    #         '3b-3c (5e14 2 MeV O$^+$ annealed)',
    #         '1a (pristine)',
    #         '1a (pristine)']

    save_name = '22light_raw_cascade_all_samples' # Cascade including all samples
    labels=['2b (3.6e16 2 MeV He$^+$ annealed)',
            '3b-3c (5e14 2 MeV O$^+$)',
            '1c-2c (8.6e15 300 keV He$^+$)',
            '2b (3.6e16 2 MeV He$^+$)',
            '2b (3.6e16 2 MeV He$^+$)',
            '1c-2c (8.6e15 300 keV He$^+$ annealed)',
            '3b-3c (5e14 2 MeV O$^+$ annealed)',
            '1a (pristine)',
            '1a (pristine)']

    plt.figure(figsize=(12, 10))

    v_shift = 0

    for x_file, y_file, label in zip(x_axis, y_axis, labels):
        # Read the data from the files
        data_wavenumber = pd.read_table(x_file)
        data_counts = pd.read_table(y_file)

        # Normalising counts
        data_counts = (data_counts - data_counts.min()) / (data_counts.max() - data_counts.min())

        # Shifting vertically
        data_counts = data_counts + 1 * v_shift
        v_shift += 1

        # Plotting iteration fo scatter graph
        plt.plot(data_wavenumber, data_counts, label=label, linewidth=1)
        plt.xlim(50, 750)

    # Adding peaks to plot
    annotate_raman_peaks('ON', 'ON', 4)

    # Naming and saving plot
    plt.title('Light region raw spectra in pristine and irradiated YBCO thin films')
    plt.legend(loc='upper right')
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Normalised Intensity (counts)')

    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\{}.png".format(save_name)
    plt.savefig(save_path)

############################ Background subtraction of selected data sets!!! #######################
## TODO: turn this subtraction into a function
background_subtraction = False
if background_subtraction:
    x_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(X-Axis).txt"))
    y_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(Y-Axis).txt"))
    save_folder = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_BackgroundSubtracted"

    poly_degree = 5
    for x_file, y_file in zip(x_axis, y_axis):

        # Reading sorted file names
        wavenumber = np.loadtxt(r"{}".format(x_file))
        counts = np.loadtxt(r"{}".format(y_file))

        # Setting counts as baseObj and running background sub
        baseObj = BaselineRemoval(counts)
        Modpoly_subtracted=baseObj.ModPoly(poly_degree)


        fig, axes = plt.subplots(1, 2, figsize=(10, 10))
        axes[0].plot(wavenumber, counts)
        axes[0].set_title('Raw Data')

        axes[1].plot(Modpoly_subtracted)
        axes[1].set_title('Modpoly (p={})'.format(poly_degree))

        # Imodpoly_subtracted=baseObj.IModPoly(poly_degree)
        # axes[2].plot(Imodpoly_subtracted)
        # axes[2].set_title('Imodpoly (p={})'.format(poly_degree))

        ## TODO: write a save_file function that saves a txt file or png. Nest this sace function in many other functions

        # Saving png file
        zipped_name = y_file[-51:-13]
        save_path = save_folder + "\\" + zipped_name + ".png"
        plt.savefig(save_path)
        plt.close(fig)

        # Zipping and saving subtracted txt file
        save_path = save_folder + "\\" + zipped_name + "Zipped-Modpoly_p={}_subtracted.txt".format(poly_degree)
        zipped = np.column_stack((wavenumber, Modpoly_subtracted))
        np.savetxt(save_path, zipped)

    print('Finished')


######################### Code snippet to plot selected SUBTRACTED raman plots on same figure #####################
subtracted_selected_cascade = False
if subtracted_selected_cascade:
    ## TODO: Turn this into a function

    zipped_subtracted_data = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_BackgroundSubtracted\*.txt"))
    # print(zipped_subtracted_data) # using to find file names to use as labels

    # save_name = '22light_raw_cascade' #Initial cascade, not including 300kev He
    # labels=['2b (3.6e16 2 MeV He$^+$ annealed)',
    #         '3b-3c (5e14 2 MeV O$^+$)',
    #         '2b (3.6e16 2 MeV He$^+$)',
    #         '2b (3.6e16 2 MeV He$^+$)',
    #         '3b-3c (5e14 2 MeV O$^+$ annealed)',
    #         '1a (pristine)',
    #         '1a (pristine)']

    save_name = '22light_subtracted_cascade_all_samples' # Cascade including all samples
    labels=['2b (3.6e16 2 MeV He$^+$ annealed)',
            '3b-3c (5e14 2 MeV O$^+$)',
            '1c-2c (8.6e15 300 keV He$^+$)',
            '2b (3.6e16 2 MeV He$^+$)',
            '2b (3.6e16 2 MeV He$^+$)',
            '1c-2c (8.6e15 300 keV He$^+$ annealed)',
            '3b-3c (5e14 2 MeV O$^+$ annealed)',
            '1a (pristine)',
            '1a (pristine)']

    plt.figure(figsize=(12, 10))
    v_shift = 1

    for file, label in zip(zipped_subtracted_data, labels):
        #print('loop running')

        # Read the data from the files
        data = np.loadtxt(file)
        data_wavenumber = data[:, 0]
        data_counts = data[:, 1]

       # print(data_wavenumber)

        # Normalising counts
        data_counts = (data_counts - data_counts.min()) / (data_counts.max() - data_counts.min())

        # Shifting vertically
        data_counts = data_counts + 1 * v_shift
        v_shift += 1

        # Plotting iteration fo scatter graph
        plt.plot(data_wavenumber, data_counts, label=label, linewidth=1)
        plt.xlim(100, 800)

    # Adding peaks to plot
    annotate_raman_peaks('ON', 'ON', 8)

    # Naming and saving plot
    plt.title('"Light region" background subtracted spectra in pristine and irradiated YBCO thin films')
    plt.legend(loc='upper right')
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Normalised Intensity (counts)')

    # plt.show()
    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\{}.png".format(save_name)
    plt.savefig(save_path)




## Code snippet to plot XRD datafiles for TA work
## TODO: edit glob so that the excel file Metal_Peak_List can be in the same folder but be ignored!!
metal_xrd_data = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\1. Metal identification\Metal_*",
                 ))
mgo_xrd_data = sorted(glob.glob(r"C:\Users\James\OneDrive - Nexus365\Paid-work-and-financial\XRD_TA_2023\2P9 XRD Data\2P9 XRD Data\2. MgO quantitative analysis\*"))

# plot_xrd(mgo_xrd_data)
# plot_xrd(metal_xrd_data)


