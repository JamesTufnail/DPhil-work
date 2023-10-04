import numpy as np
import glob

def normalising_to_max(data):
    norm_data = (data - data.min()) / (data.max() - data.min())
    return norm_data

def raman_zipping(x_axis, y_axis, save_folder):
    """ JT - Function to take the MRF raman files in x-axis and y-axis form and zip them together into one .txt file.
    This is to be used on the selected data that you want to use in Origin.

    :param x_axis: file path of X-Axis Raman data
    :param y_axis: file path of Y-Axis Raman data
    :param save_folder: file path of 'Zipped Files for Origin' folder
    :return: saves as .txt file of zipped file with filename
    """

    counts = np.loadtxt("{}".format(y_axis))
    wavenumber = np.loadtxt("{}".format(x_axis))

    norm_counts = normalising_to_max(counts)
    # zipped_name = y_axis[-51:-13]
    save_path = save_folder + "\\" + zipped_name + ".txt"


    zipped = np.column_stack((wavenumber, norm_counts))

    np.savetxt(save_path, zipped)

    print('Zipping of file {} is complete.'.format(zipped_name))


save_folder = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Gd\2MeVHe\cropped and subbed"
zipped_name = 'Fu21Gd_2MeV_He_5point_avg'
x_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Gd\2MeVHe\cropped and subbed\2 Average of 5 Spectra (Average 5) (B+R) (Average 5) (Sub BG) (X-Axis).txt"
y_axis = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Gd\2MeVHe\cropped and subbed\2 Average of 5 Spectra (Average 5) (B+R) (Average 5) (Sub BG) (Y-Axis).txt"
raman_zipping(x_axis, y_axis, save_folder)
