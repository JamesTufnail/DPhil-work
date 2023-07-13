import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

def xas_spectra_plot(data, edge_start, h_line, title):

    for i, file in enumerate(data):
        plt.plot(data[i, 0], data[i, 1], labels=data[i, 2])

    if h_line:
        plt.axhline(y=0, linestyle='--', color='black')

    plt.legend()
    plt.title(title)
    plt.xlim(8975 - edge_start, 35)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Intensity')
    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised" + '\\' + title
    plt.savefig(save_path)
    plt.close()


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

def find_title_from_filename(filename, character, start, stop):
    """JT - Function to find the title of a file based on certain charactres in a filename.
    INPUTS: filename, character (what to search for, e.g. '_'), start (how many values after character to start at),
    stop (how many values from the end to include).
    OUTPUTS: title
    e.g. find_title_from_filename(mawatari_files[0], '_', 1, -4) takes file 0 from mawatari files, looks
    through the filename until it finds the last case of _ and then names the file the letter after _ until -4
    letters from the end."""

    filename_id = filename.rfind('{}'.format(character))
    title = filename[filename_id + start:stop]
    return title