"""
Version: 1.0
date: 25/03/2024
author: James Tufnail

This file currently calculates and plots the real and imaginary parts of magnetic sucseptibility (X' and X'') for a given sample. 
The data is extracted from the Susceptibility_Measurements.dat file, which is located in the PPMS Data folder of the sample folder. 
The data is then plotted as a function of temperature for each magnetic field value. 
The function also calculates the irreversibility field (Birr) as the temperature at which the real part of the susceptibility is maximised.

- Add Tc to the susceptibility plot, and adjust x'' axis values
- Added save option to save to a 'Figures' folder in the sample folder

TODO:
- Add Tc error
- Automatically write Tc to a text file in the sample folder

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
from functions import *
from scipy.stats import linregress
from scipy.optimize import minimize

################### Defining functions ####################

def find_ix_by_sample_offset(data):
    """
    Function to find the index of the data where the sample offset is recorded. This is used to index through the data to find the start of each measurement

    Parameters:
    data (pd.DataFrame): Dataframe containing the data

    Returns:
    ix (list): List of indices where the sample offset is recorded
    """

    ix=[]
    for i in range(len(data)):
        if 'sample offset' in data['Comment'][i]:
            ix.append(i)

    ix.append(data.index[-1]) # ensure last measurement is included

    return ix


def plot_susceptibility(data, ix, sample_name, tc, save_path, save=False):

# Plotting the susceptibility and recording Birr
    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8, 6))

    # Initialising lists to store magnetic field
    field = []

    for index, i in enumerate(ix):
        if index < len(ix) - 1:
            start = ix[index]
            end = ix[index + 1] 
            field.append(abs(data['Magnetic Field (T)'][i].round(2)))

            axs[1].scatter(data['Temperature (K)'][start:end], data["AC X'  (emu/Oe)"][start:end], label = '{} T'.format(field[index]), s=5)
            axs[0].scatter(data['Temperature (K)'][start:end], data['AC X" (emu/Oe)'][start:end], label = '{} T'.format(field[index]), s=5)

    # Plotting susceptibility data
    axs[0].set_title(f'AC Susceptibility for the {sample_name} sample')
    axs[0].set_ylim(0, )
    axs[1].set_xlabel('Temperature (K)'), axs[1].set_ylabel('AC X\' (emu/Oe)')
    axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0)), axs[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[0].set_ylabel('AC X" (emu/Oe)')
    axs[0].legend(loc='upper left')
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.1)

    # Adding Tc to the plot
    plt.text(0.05, 0.8, 'Tc = {} K'.format(round(tc, 2)),
             transform=plt.gca().transAxes, fontsize=10, ha='left', va='center',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    if save:
        save_path = os.path.join(save_path, 'New Figures')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.savefig(os.path.join(save_path, f'Birr_vs_Magnetic_Field_{sample_name}.png'))
        plt.close()
    else:
        plt.show()

    return 

def plot_Birr(data, ix, sample_name, save_path, bc2 = True, save=False):

    field, Birr = [], []
    for index, i in enumerate(ix):
        if index < len(ix) - 1:
            start = ix[index]
            end = ix[index + 1] 
            field.append(abs(data['Magnetic Field (T)'][i].round(2)))

            # Finding Birr as the temperature at which the real part of the susceptibility is maximised
            for j in range(start, end):
                if data['AC X" (emu/Oe)'][j] == max(data['AC X" (emu/Oe)'][start:end]):
                    Birr.append(data['Temperature (K)'][j])
   
    if bc2:
        plt.scatter(Birr, field, label='Raw')
        x = np.linspace(Birr[0], Birr[-1], 100)
        Bc2 = 152.6*(1 - np.array(x)/85.8)**1.49
        plt.plot(x, Bc2, label=r'$B_{c2} = 152.6\left(1 - \frac{T}{85.8}\right)^{1.49}$')
        plt.legend()
    else:
        plt.scatter(Birr, field)

    plt.title(f'Birr vs. Magnetic Field for {sample_name} sample')
    plt.xlabel('Temperature (K)'), plt.ylabel('Magnetic Field (T)')
    

    if save:
        save_path = os.path.join(save_path, 'New Figures')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.savefig(os.path.join(save_path, f'Birr_vs_Magnetic_Field_{sample_name}.png'))
        plt.close()
    else:
        plt.show()

    return

def get_sample_names(folder_path):
    """
    Function to return the list of folder names in the specified path. Use to get the list of the sample names

    Parameters:
    folder_path (str): Path to the folder containing the sample folders (e.g. ...Experiments\Birmingham Neutron Irradiation\Birmingham data\data-for-manipulation-pristine-measurements
    
    Returns:
    sample_names (list): List of sample (and folder) names in the specified path
    """
    sample_names = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            sample_names.append(item)

    return sample_names 

def open_data(data_path, sample_name):
    """
    Function to open the data for a specific sample. The function uses the glob module to search for the data in the specified path

    Parameters:
    data_path (str): Path to the data file
    sample_name (str): Name of the sample to search for

    Returns:
    data (pd.DataFrame): Dataframe containing the data for the specified sample
    """

    # Opening file path
    data_file_pattern = os.path.join(data_path, sample_name, 'Irr0', 'PPMS Data') + '\**\Susceptibility_Measurements.dat'
    file_path = glob.glob(data_file_pattern, recursive=True)[0]
    print('Sample is:', sample_name)
    print('Data path is:', file_path)

    # Saving file path
    save_path_pattern = os.path.join(data_path, sample_name, 'Irr0', 'PPMS Data')
    save_path = glob.glob(save_path_pattern + '\*', recursive=True)[0]
    print('Save path is:', save_path)
    # print(save_path_pattern)


    # Extract the data
    data = pd.read_csv(file_path, header=33, usecols=[0,2,3,10,11])
    data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)']/10000)
    data['Comment'] = data['Comment'].astype(str)

    return data, save_path

def find_tc_interpolation(data, ix, show_plot = True):
    # Plotting raw data
    start, end = ix[0], ix[1] # Ix for all
    start_norm, end_norm = ix[0], ix[0] + 10 # Ix for normal state
    start_trans, end_trans = ix[0] + 15, ix[0] + 20 # Ix for transition state

    # Slicing interp ranges
    temp, sus = data['Temperature (K)'][start:end], data["AC X'  (emu/Oe)"][start:end]
    temp_fit_norm, sus_fit_norm = data['Temperature (K)'][start_norm:end_norm], data["AC X'  (emu/Oe)"][start_norm : end_norm]
    temp_fit_trans, sus_fit_trans = data['Temperature (K)'][start_trans:end_trans], data["AC X'  (emu/Oe)"][start_trans:end_trans]
    # print('Start:', start, 'End:', end)
    
    # Fitting normal region
    slope_norm, intercept_norm, r, p, se = linregress(temp_fit_norm, sus_fit_norm)
    x_norm = np.linspace(temp.iloc[0], temp.iloc[-1], 10000)
    
    # Fitting transition region
    slope_trans, intercept_trans, r, p, se = linregress(temp_fit_trans, sus_fit_trans)
    x_trans = np.linspace(temp.iloc[0], temp.iloc[-1], 10000)
    
    # Find the intersection between the normal state and transition lines
    initial_guess = [90, 0] # Initial guess for the intersection point (can be any point)
    normal_params = slope_norm, intercept_norm
    transition_params = slope_trans, intercept_trans
    result = minimize(line_difference, initial_guess, args=(normal_params, transition_params), tol=1e-6,
                      options = {'disp' : True}) # Minimize the difference function
    tc_x, tc_y = result.x # Extract the intersection point
    print('Tc =', tc_x, ' K')

    # Plotting the data
    if show_plot:
        y_norm = slope_norm*x_norm + intercept_norm
        y_trans = slope_trans*x_trans + intercept_trans
        plt.scatter(temp, sus) 
        plt.plot(x_norm, y_norm)  
        plt.plot(x_trans, y_trans)
        plt.ylim(1.1*sus.min() , 1e-4)
        plt.text(0.05, 0.8, 'Tc = {} K'.format(round(tc_x, 3)),
             transform=plt.gca().transAxes, fontsize=10)
        plt.show()
    else:
        pass

    return tc_x


########################### Main Script ########################
save = False
bc2 = False
show_plot = True



# Specify the path to the folder with sample names
folder_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Birmingham Neutron Irradiation\Birmingham data\data-for-manipulation-pristine-measurements"
# Specify the path to the data
data_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Birmingham Neutron Irradiation\Birmingham data\data-for-manipulation-pristine-measurements"



# Acquire and print sample names
sample_names = get_sample_names(folder_path) 
# print('Sample names are:', sample_names) 




# Loop to plot the data for each sample
# for sample in sample_names:
    # data, save_path = open_data(data_path, sample) # navigates to sample\Irr0\PPMS Data\Susceptibility_Measurements.dat and extracts data
    # ix = find_ix_by_sample_offset(data) # finds the index of the data where the sample offset is recorded
    # # plot_susceptibility(data, ix, sample_name=sample, save_path = save_path, save = False) # plots the susceptibility data for the sample
    # # plot_Birr(data, ix, sample_name=sample, save_path=save_path, bc2=bc2, save=save)
    # break


for sample in sample_names:
    data, save_path = open_data(data_path, sample) # navigates to sample\Irr0\PPMS Data\Susceptibility_Measurements.dat and extracts data
    ix = find_ix_by_sample_offset(data)
    tc = find_tc_interpolation(data, ix, show_plot = show_plot)
    plot_susceptibility(data, ix, sample_name=sample, save_path = save_path, tc = tc, save = False) # plots the susceptibility data for the sample
    plot_Birr(data, ix, sample_name=sample, save_path=save_path, bc2=bc2, save=save)

    # plt.show()
    break



# Load the data
# data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\PPMS\practice_data_for_scripting\Fu21Gd_practice\Susceptibility_Measurements.dat", 
#                    header=33, usecols=[0,2,3,10,11])
# data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)']/10000)
# data['Comment'] = data['Comment'].astype(str)