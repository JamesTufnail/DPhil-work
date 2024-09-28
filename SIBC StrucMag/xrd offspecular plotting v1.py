"""
xrd offspecular plotting v1.py
James Tufnai
16/07/2024

This script is used to plot off-specular XRD data from the empyrean XRD in the CFAS lab.

The data is read in from a .csv file and plotted in 3D and 2D contour plots.

The script is designed to be used with the following file structure:
- XRD data in SIBC project
- ab axis folder
- all .csv files of the off-specular data (4 in total) for a given sample
being 029, 0210, 309, 3010 reflections.

Actions:
- Set Save boolean
- Set the sample name
- Set the save and sample (data file) locations
- Set the labels for the data (0210, 029, 3010, 309 reflections) in the order they are read in.
NOTE: check the data is read by print statement and adjust if there are missing reflections
- Comment through sample types (a,b,c)
- Comment out scripts at bottom to decide what you want to plot


To-Do:
- Add in the ability to read in the labels from the file names
- Add method of identifying peaks in the data and annotating them on the plots
"""

import matplotlib.pyplot as plt
import pandas as pd
import glob

##### Variable Magic ########
save = True # Set save to True to save the plots
save_location = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\figures - off-specular"

# sample = 'Fu21Gd-SM1c' # including a,b,c notation
# sample = 'SuNAM21Gd-SM2c' # including a,b,c notation
sample = 'SP11-SM3c' # including a,b,c notation

# folder of the data (containing all ab .csv files)
sample_location = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\ab axis"

labels = ['0210 Reflection', '029 Reflection', '3010 Reflection', '309 Reflection'] # have to label this way as that's the way the code rads in the data


####### Permanent code from hereon in ##########

files = glob.glob(sample_location + '\\' + sample + '*.csv')

# check files are being read in in the correct order.
for file in files: print(file[-20:]) 
print('Are files read in in the same order as label? \n i.e.:', labels)

##### Plotting functions ########
def offspecular_3d_plot(files, labels, sample, save=False, save_location=None):
    fig = plt.figure(figsize=(12, 12))

    for i, (file, label) in enumerate(zip(files, labels)):
        data = pd.read_csv(file, delimiter=',', header=31)
        
        ax = fig.add_subplot(2, 2, i+1, projection='3d')

        x = data['2Theta position']
        y = data[' Omega position']
        z = data[' Intensity']

        trisurf = ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

        ax.set_xlabel(r'2$\theta$ position (deg)')
        ax.set_ylabel('$\omega$ position (deg)')
        # ax.set_zlabel('Intensity')

        colorbar = fig.colorbar(trisurf, ax=ax, shrink=0.5, aspect=10)
        colorbar.set_label('Intensity')

        ax.set_title(label)

    plt.suptitle('Offspecular XRD Scans for {}'.format(sample), fontsize=16)
    plt.tight_layout(pad=4)

    # Adjust layout with additional space between rows
    plt.subplots_adjust(hspace=0.3)

    if save:
        fig.savefig(save_location + '\\3D plots\\' + sample + ' offspecular.png', dpi=300)

    else:
        plt.show()

def offspecular_3d_plot_individual(files, labels, sample, save=False, save_location=None):
    

    for i, (file, label) in enumerate(zip(files, labels)):
        data = pd.read_csv(file, delimiter=',', header=31)
        
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection='3d')

        x = data['2Theta position']
        y = data[' Omega position']
        z = data[' Intensity']

        trisurf = ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

        ax.set_xlabel(r'2$\theta$ position (deg)')
        ax.set_ylabel('$\omega$ position (deg)')
        # ax.set_zlabel('Intensity')

        fig.suptitle('Offspecular XRD Scans for {}'.format(sample + '-' + label), fontsize=16)
        plt.tight_layout()
        # Add color bar
        colorbar = fig.colorbar(trisurf, ax=ax, shrink=0.5, aspect=10)
        colorbar.set_label('Intensity')

        if save:
            fig.savefig(save_location + '\\3D plots\\' + sample + '-' + label + ' - offspecular.png', dpi=300)
        else:
            plt.show()

def offspecular_2d_contour_individual(files, labels, sample, save=False, save_location=None):
    for file, label in zip(files, labels):
        data = pd.read_csv(file, delimiter=',', header=31)
        
        fig = plt.figure(figsize=(6,6))
        ax2d = fig.add_subplot(111)

        x = data['2Theta position']
        y = data[' Omega position']
        z = data[' Intensity']

        # Make plot
        contour = ax2d.tricontourf(x, y, z, cmap='viridis')
        ax2d.set_xlabel(r'2$\theta$ position (deg)')
        ax2d.set_ylabel('$\omega$ position (deg)')


        # Find the maximum intensity and its coordinates
        """ Can try and fix this later """
        # max_idx = z.idxmax()
        # max_x = x[max_idx]
        # max_y = y[max_idx]
        # max_z = z[max_idx]

        # # Annotate the maximum point
        # ax2d.scatter(max_x, max_y, color='red', marker = 'x')
        # ax2d.text(max_x + 0.5, max_y, f'({max_x:.2f}, {max_y:.2f})', color='red')

        fig.suptitle('Offspecular XRD Contour for {}'.format(sample + '-' + label), fontsize=12)
        plt.tight_layout()
        plt.grid(True)

        # Add color bar for the 2D plot
        colorbar = fig.colorbar(contour, ax=ax2d, shrink=0.5, aspect=10)
        colorbar.set_label('Intensity')

        if save:
            fig.savefig(save_location + '\\Contour Plots\\' + sample + '-' + label + '-offspecular_2d.png', dpi=300)
            plt.close(fig)
        else:
            plt.show()

def offspecular_2d_contour(files, labels, sample, save=False, save_location=None):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    for ax, file, label in zip(axs.ravel(), files, labels):
        data = pd.read_csv(file, delimiter=',', header=31)

        x = data['2Theta position']
        y = data[' Omega position']
        z = data[' Intensity']

        # Make plot
        contour = ax.tricontourf(x, y, z, cmap='viridis')
        ax.set_xlabel(r'2$\theta$ position (deg)')
        ax.set_ylabel('$\omega$ position (deg)')

        # # Find the maximum intensity and its coordinates
        # max_idx = z.idxmax()
        # max_x = x[max_idx]
        # max_y = y[max_idx]
        # max_z = z[max_idx]

        # # Annotate the maximum point
        # ax.scatter(max_x, max_y, color='red', marker='x')
        # ax.text(max_x + 0.5, max_y, f'({max_x:.2f}, {max_y:.2f})', color='red')

        ax.set_title('{}'.format(label), fontsize=12)

        # Add color bar for the 2D plot
        colorbar = fig.colorbar(contour, ax=ax, shrink=0.5, aspect=10)
        colorbar.set_label('Intensity')

    fig.suptitle('Offspecular XRD Contours for {}'.format(sample), fontsize=16)
    plt.tight_layout(pad=4)

    # Adjust layout with additional space between rows
    plt.subplots_adjust(hspace=0.3)

    if save:
        fig.savefig(save_location + '\\Contour Plots\\' + sample + '-offspecular_2d.png', dpi=300)
        plt.close(fig)
    else:
        plt.show()



########### Script ###########

# offspecular_3d_plot(files, labels, sample, save=save, save_location=save_location)
# offspecular_3d_plot_individual(files, labels, sample, save=save, save_location=save_location)

offspecular_2d_contour_individual(files, labels, sample, save=save, save_location=save_location)
offspecular_2d_contour(files, labels, sample, save=save, save_location=save_location)

print('Finished plotting.')


