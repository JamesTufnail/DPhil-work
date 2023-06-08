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
    save_path = save_folder + "\\" + zipped_name +".txt"

    zipped = np.column_stack((wavenumber, counts))

    np.savetxt(save_path, zipped)

    print('Zipping of file {} is complete.'.format(zipped_name))

def plot_raman_separate_files(x_axis, y_axis, title, save_path):
    """JT - Function to plot Raman data when presented in two datasets
        INPUTS: x_axis, y_axis, """

    data_wavenumber = pd.read_table("{}".format(x_axis), header=None, names=["Wavenumber"])
    data_counts = pd.read_table("{}".format(y_axis), header=None, names=["Counts"])

    # Normalising counts
    data_counts['Counts'] = (data_counts['Counts'] - data_counts[
        'Counts'].min()) / (data_counts['Counts'].max() - data_counts['Counts'].min())

    plt.plot(data_wavenumber['Wavenumber'], data_counts['Counts'], linewidth=1)

    # Just using title to figure out which plots to delete
    # title = x_axis[-30:]
    plt.title("{}".format(title))

    plt.savefig(save_path)
    #plt.show()
    plt.close()

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
    for x_file, y_file in zip(wavenumbers,counts):
        data_wavenumber = pd.read_table(x_file)
        data_counts = pd.read_table(y_file)

        # Normalising counts
        data_counts = (data_counts - data_counts.min()) / (data_counts.max() - data_counts.min())

        # Shifting vertically
        data_counts = data_counts + 1*v_shift
        v_shift+=1

        # Plotting iteration fo scatter graph
        plt.plot(data_wavenumber, data_counts, label='{}'.format(x_file[-36:-26]), linewidth=1)
        plt.xlim(50, 750)

    plt.title("{}".format(title))
    plt.legend(loc='upper right')
    plt.savefig(save_path)
    plt.close()
    #plt.show()
    print('Cascade Raman Plot run succesfully and saved in {}'.format(save_path))



def annotate_raman_peaks(verticals, labels, annotate_height):
    # plotting verticals
    if verticals == 'ON':
        plt.axvline(x=Ba_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=Cu2_freq, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq1, ls='--', lw='0.5', color='black')
        plt.axvline(x=O2_O3_freq2, ls='--', lw='0.5', color='black')
        plt.axvline(x=O4_freq, ls='--', lw='0.5', color='black')
    # Adding annotation arrows for known peaks
    if labels == 'ON':
        plt.annotate('Ba', xy=(Ba_freq, annotate_height), xytext=(Ba_freq - 55, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('Cu(2)', xy=(Cu2_freq, annotate_height), xytext=(Cu2_freq + 60, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)-', xy=(O2_O3_freq1, annotate_height), xytext=(O2_O3_freq1 - 90, annotate_height - 0.1),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(2)+/O(3)+', xy=(O2_O3_freq2, annotate_height), xytext=(O2_O3_freq2 - 90, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))
        plt.annotate('O(4)', xy=(O4_freq, annotate_height), xytext=(O4_freq + 60, annotate_height),
                     arrowprops=dict(facecolor='black', headwidth=5, headlength=5, width=2))