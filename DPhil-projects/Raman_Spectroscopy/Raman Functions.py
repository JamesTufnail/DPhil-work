import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

# File contains Raman plotting and other related functions

# Inputting known values of pristine peaks taken from Thompsen and Kaczmaryzek
Ba_freq = 115
Cu2_freq = 150
O2_O3_freq1 = 334
O2_O3_freq2 = 438
O4_freq = 502


def normalising_to_max(data):
    norm_data = (data - data.min()) / (data.max() - data.min())
    return norm_data


def normalising_to_tail(data):
    """ JT - Must use .iloc if using Dataframe

    :param data:
    :return:
    """
    norm_data = (data - data.min()) / (data.iloc[-1] - data.min())
    return norm_data


def raman_zipping(x_axis, y_axis, save_folder):
    """ JT - Function to take the MRF raman files in x-axis and y-axis form and zip them together into one .txt file.
    This is to be used on the selected data that you want to use in Origin.

    :param x_axis: file path of X-Axis Raman data
    :param y_axis: file path of Y-Axis Raman data
    :param save_folder: file path of 'Zipped Files for Origin' folder
    :return: saves as .txt file of zipped file with filename
    """
    counts = np.loadtxt(r"{}".format(x_axis))
    wavenumber = np.loadtxt(r"{}".format(y_axis))

    zipped_name = y_axis[-51:-13]
    save_path = save_folder + "\\" + zipped_name + ".txt"

    zipped = np.column_stack((wavenumber, counts))

    np.savetxt(save_path, zipped)

    print('Zipping of file {} is complete.'.format(zipped_name))


def plot_raw_raman_cascade(x_file_names, y_file_names, title, save_path):
    """JT - Function that takes list of input file names (with * if necessary), normalises the y
    values, shifts each iteration vertically by 1 and plots them all on the same cascade plot.
        INPUTS: x_file_names (name of file with x values in), y_file_names (name of file with y values in)
       """

    # Reading in file names
    wavenumbers = sorted(glob.glob("{}".format(x_file_names)))
    counts = sorted(glob.glob("{}".format(y_file_names)))

    v_shift = 0

    plt.figure(figsize=(10, 12))

    # Iterates over the x and y files, zipping them together into a single array. Then normalises them,
    # and shifts each iteration vertically by 1. Names each iteration plotted on graph
    for x_file, y_file in zip(wavenumbers, counts):
        data_wavenumber = pd.read_table(x_file)
        data_counts = pd.read_table(y_file)

        # Normalising counts
        data_counts = (data_counts - data_counts.min()) / (data_counts.max() - data_counts.min())

        # Shifting vertically
        data_counts = data_counts + 1 * v_shift
        v_shift += 1

        # Plotting iteration fo scatter graph
        plt.plot(data_wavenumber, data_counts, label='{}'.format(x_file[-36:-26]), linewidth=1)
        plt.xlim(50, 750)

    plt.title("{}".format(title))
    plt.legend(loc='upper right')
    plt.savefig(save_path)
    plt.close()
    # plt.show()
    print('Cascade Raman Plot run succesfully and saved in {}'.format(save_path))


def annotate_raman_peaks(verticals, labels, annotate_height):

    # plotting verticals
    if verticals == 'True':
        #plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
        plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')

    # Adding annotation arrows for known peaks
    if labels == 'True':
        #plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
         #            arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('Cu(2)', xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 0.5),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height +0.5),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))

def raman_zip_and_plot(directory, save_dir, title, label):
    """

    :param title: title
    :param label: label of plot
    :param directory: file path of directory containing x and y
    :return:
    """

    x_file = glob.glob(r"{}\\*(X-Axis).txt".format(directory))[0]
    y_file = glob.glob(r"{}\\*(Y-Axis).txt".format(directory))[0]

    counts = np.loadtxt(x_file)
    wavenumber = np.loadtxt(y_file)
    zipped = np.column_stack((counts, wavenumber))
    data = pd.DataFrame(zipped)
    data.columns = ["Wavenumber", "Counts"]

    # Normalising counts
    data['Counts'] = (data['Counts'] - data['Counts'].min()) / (data['Counts'].max() - data['Counts'].min())

    data.to_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\_Processed\_all_zipped_normalised_data"
                + "\\" + title + " - " + label + ".csv", index=False) # Saving in collective directory
    data.to_csv(directory + "\\" + title + " - " + label + ".csv", index=False) # Saving in load directory
    data.to_csv(save_dir + "\\" + title + " - " + label + ".csv", index=False) # Saving in save directory

    plt.plot(data['Wavenumber'], data['Counts'], linewidth=1, label = label)
    plt.title(title)
    plt.legend()
    plt.xlabel('Wavenumber')
    plt.ylabel('Normalized Counts')
    # plt.show()

    plt.savefig(directory + "\\" + title + " - " + label + ".png")
    plt.savefig(save_dir + "\\" + title + " - " + label + ".png")
    plt.savefig(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\James Tufnail - YBCO thin films\_Processed\_all_python_plots" + "\\" + title + " - " + label + ".png")
    plt.close()


def raman_cascade(directory, save_dir, title):
    # Reading in files
    files = glob.glob(r"{}\\*".format(directory))

    order = [0,3,1,2] # For resetting the order in the cascade plot
    files = [files[i] for i in order]


    shifts = range(len(files))

    # plt.figure(figsize=(24, 24))

    for file, index in zip(files, shifts):
        df = pd.read_csv(file)
        wavenumber = df["Wavenumber"]
        counts = df["Counts"]

        plt.plot(wavenumber, counts + 1*index, linewidth=1)

    plt.title(title)
    plt.xlim(0, 800)
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Relative Intensity')

    #annotate_raman_peaks("True", "True", 4) # using annotate peaks function to run

    # plt.legend(loc='upper right')
    # plt.savefig(save_path)
    plt.savefig(save_dir + "\\" + title + ".png")
    plt.savefig(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO thin films\_Processed\_all_python_plots" + "\\" + title + ".png")

    plt.close()
    # plt.show()
    # print('Cascade Raman Plot run succesfully and saved in {}'.format(save_path))

def nor_to_txt(glob_locations, skips):
    """ JT - Converts .nor files from Athena into .txt files with energy and normalised counts

    :param skips: number of rows of .nor file to skip
    :param glob_locations: file location including * of data
    :return:
    """

    filenames = glob.glob(r"{}".format(glob_locations))

    for file in filenames:
        data = pd.read_csv(file,
                           skiprows = skips, delim_whitespace=' ', usecols= [0, 1])
        data.columns = ["Energy", "Normalised Counts"]

        start_name = file.rfind('diff')
        end_name = file.rfind('.nor')
        name = file[start_name : end_name]

        savename = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Exported Athena Data\Fu21 and Sp11 diff plots as txt" + '\\' + name + '.txt'

        data.to_csv(savename, index=False)
