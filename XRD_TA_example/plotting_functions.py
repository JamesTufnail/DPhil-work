import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_xrd(filenames):
    """ JT -  Functon to plot XRD angle vs intensity data
    INPUTS: filename = array of filenames of datasets"""
    ## TODO: change these to have a more general format, not just one row

    n_files = len(filenames)
    fig, axes = plt.subplots(nrows=n_files, ncols=1)

    for index, file in enumerate(filenames):
        data = pd.read_csv(file, header=None, names=["Angle", "Intensity"])

        ax = axes[index]
        ax.plot(data["Angle"], data["Intensity"])

        # Searching filename for the last occurence of \, to then label it properly
        filename_id = file.rfind('\\')
        ax.set_title('{}'.format(file[filename_id + 1:]))

    fig.text(0.5, 0.04, r"Angle (2$\theta)$)", ha='center', va='center')
    fig.text(0.06, 0.5, "Intensity (cps)", ha='center', va='center', rotation='vertical')

    plt.show()
    print('plot_xrd function has finished for data in {}'.format(filenames))


def plot_raman_separate_files(x_axis, y_axis, verticals, labels):
    """JT - Function to plot Raman data when presented in two datasets
        INPUTS: x_axis, y_axis, verticals=(ON/OFF), labels=(ON/OFF)"""

    data_wavenumber = pd.read_table("{}".format(x_axis), header=None, names=["Wavenumber"])
    data_counts = pd.read_table("{}".format(y_axis), header=None, names=["Counts"])

    # Normalising counts
    data_counts['Counts'] = (data_counts['Counts'] - data_counts[
        'Counts'].min()) / (data_counts['Counts'].max() - data_counts['Counts'].min())

    plt.plot(data_wavenumber['Wavenumber'], data_counts['Counts'], linewidth=1)

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


def plot_scatter(filename, title, x_axis, y_axis):
    """JT - general scatter plotting function.
    Inputs: filename, title, x_axis, y_axis"""
    data = np.loadtxt(fname=filename, delimiter=',')

    plt.scatter(data)

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)

    plt.show()
    print('Scatter function has run succesfully for {}.'.format(filename))
