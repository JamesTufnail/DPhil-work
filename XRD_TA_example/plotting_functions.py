import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_xrd(filename, title='XRD Plot'):
    """JT -  Functon to plot XRD angle vs intensity data
    INPUTS: filename, title (default title is XRD plot)"""

    data = pd.read_csv("{}".format(filename), header=None, names=["Angle", "Intensity"])
    angle = data["Angle"]
    intensity = data["Intensity"]

    plt.plot(angle, intensity, label='%s data' % filename)
    plt.xlabel(r"Angle (2$\theta$)")
    plt.ylabel("Intensity (cps)")
    plt.title('{}'.format(title))

    plt.show()
    print('plot_XRD has run for {}'.format(filename))



def plot_raman_separate_files(x_axis, y_axis, verticals, labels):
    """JT - Function to plot Raman data when presented in two datasets - e.g. from MRF raman.
     INPUTS: x_axis data, y_axis data, verticals (ON/OFF) add vertical lines at peaks, labels (ON/OFF) are the same"""

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
    print('Scatter function has run successfully for {}.'.format(filename))