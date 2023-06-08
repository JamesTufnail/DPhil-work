
from raman_functions import *
from PycharmProjects.mawatari_practice.mawatari_functions import *
from developing_functions import *
from misc_functions import *
import glob
from BaselineRemoval import BaselineRemoval

## TODO: Plot all raw raman files and compare different samples with same parameters. Then plot same parameters but different samples together on cascade plot
## TODO: use a background subtraction and replot them all


## Background subtraction of selected data sets!!! ##
## TODO: turn this subtraction into a function

x_axis = sorted(glob.glob(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(X-Axis).txt"))
y_axis = sorted(glob.glob(
    r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(Y-Axis).txt"))
save_folder = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_BackgroundSubtracted"

poly_degree = 5
for x_file, y_file in zip(x_axis, y_axis):

    # Reading sorted file names
    counts = np.loadtxt(r"{}".format(x_file))
    wavenumber = np.loadtxt(r"{}".format(y_file))

    # Setting counts as baseObj and running background sub
    baseObj = BaselineRemoval(wavenumber)
    Modpoly_subtracted=baseObj.ModPoly(poly_degree)


    fig, axes = plt.subplots(1, 2, figsize=(10, 10))
    axes[0].plot(counts, wavenumber)
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





#### Code snippet to plot selected raman plots on same figure ##
raw_selected_cascade = False
if raw_selected_cascade:
    ## TODO: Turn this into a function
    ### Make these the inputs to the function, you also need a function that will tell you the order so that yoy can choose the labelling
    x_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(X-Axis).txt"))
    y_axis = sorted(glob.glob(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\Setting22_light_RAW\*(Y-Axis).txt"))

    #print(y_axis)
    labels=['2b (3.6e16 2MeV He annealed)', '3b-3c (5e14 2MeV O$^+$)', '2b (3.6e16 2 MeV He)', '2b (3.6e16 2MeV He)', '3b-3c (5e14 2MeV O$^+$ annealed)', '1a (pristine)', '1a (pristine)']

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

    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light\22light_raw_cascade.png"
    plt.savefig(save_path)



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


