"""
Version 1.0
Date: 2024-04-23
Author: James Tufnail
james.tufnail@materials.ox.ac.uk

Description:
Code will take an input excel file containing magnetisation data and plot the raw mawatari loop. 
The code will then interpolate the data so that the top and bottom halves of the mawatari loop have the same field values.
The code will then calculate the delta magnetisation between the top and bottom halves of the mawatari loop. 
The code will then calculate the critical current density (jc) and plot jc vs field.

Requirements:
Data must be in an excel spreadsheet with the columns labelled 'Field [T]' and 'Moment [emu]'

Recommended reading:
- Mawatari et al. 1997 Field sweep rate dependence of magnetization and current-voltage characteristics in superconducting disks 
https://www.sciencedirect.com/science/article/pii/S0921453497012045


To-do for version 1.1
- Add neater interpolation functions
- Add different sample dimensions (e.g. disc sample)
- Add option to plot multiple samples on the same graph
- Include other plotting functions (e.g. E-J, B-T, suscpetibility vs T)

Thanks :) 
"""

#### Importing libraries ####
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp

#### Defining functions #####
def read_and_convert(datafile):
    """ Function to read in the data and convert emu to A m2

    Args:
    datafile: string, path to the data file

    Returns:
    data: pandas dataframe
    """
    data = pd.read_excel(datafile, header=0) # Read in the data
    data.insert(2, 'DC Moment [A m2]', data['Moment [emu]'] * 1e-3) # convert emu to A m2

    return data

def plot_raw_mawatari_loop(data, sample_name):
    """
    Function plots raw mawatari loop

    Args:
    data: pandas dataframe (need to have columns 'Field [T]' and 'DC Moment [A m2]')

    Returns:
    plot of raw mawatari loop
    """
    plt.figure(figsize=(8, 4))
    plt.scatter(data['Field [T]'], data['DC Moment [A m2]'], s=2.5)
    plt.axhline(y=0, color='grey', linestyle='--')
    # plt.legend(loc='upper right')
    plt.title('Raw Mawatari Loop for the {} sample'.format(sample_name))
    plt.xlabel('Field [T]')
    plt.ylabel('Magnetisation (A m$^2$)')
    plt.show()

def plot_jc_vs_field(fields_interpolated, jc):
    """ Function to plot jc vs field

    Args:
    fields_interpolated: numpy array of field values that have been interpolated
    jc: numpy array of jc values

    Returns:
    plot of jc vs field    
    """
    plt.loglog(fields_interpolated, jc)
    plt.grid(True)
    plt.xlabel('Field [T]')
    plt.ylabel('Jc [A/m^2]')
    plt.title('Jc vs Field for {}'.format(sample_name))
    plt.show()

    return None


def interpolate_data(data):
    """ Function to interpolate the data so that the top and bottom halves of the mawatari loop have the same field values
    """

    # Finding the index of the middle of the data to subsection when finding the top and bottom halves of the mawatari loop
    mid_ix = len(data) // 2

    # dropping data points where the field is negative so that we can extract jc
    data = data.drop(data[data['Field [T]'] < 0].index)
    data = data.reset_index(drop=True)

    # extract field and moment columns
    field, moment = data['Field [T]'], data['DC Moment [A m2]']


    # Finding indices of the first and last zero fields, and the max field
    first_0_field_ix, second_0_field_ix = data['Field [T]'][0:mid_ix].idxmin(), data['Field [T]'][mid_ix:].idxmin()
    # max_field_ix = data['Field [T]'].idxmax()

    # Splitting the data into bottom and top halves based on indices and then interpolating so we can have the same field values
    bottom_B, bottom_m = field[first_0_field_ix:mid_ix], moment[first_0_field_ix:mid_ix]
    top_B, top_m = field[mid_ix:second_0_field_ix], moment[mid_ix:second_0_field_ix]

    # Interpolating the field values so that we can have the same field values for the top and bottom magnetisation values
    fields_interpolated = np.linspace(bottom_B.min(), bottom_B.max(), 1000)

    # calculating the interpolation functions for the top and bottom halves of the mawatari loop
    bottom_interp_func = interp.interp1d(bottom_B, bottom_m, kind='linear', fill_value='extrapolate') 
    top_interp_func = interp.interp1d(top_B, top_m, kind='linear', fill_value='extrapolate')

    # Interpolating the magnetisation values
    mag_interp_bottom = bottom_interp_func(fields_interpolated)
    mag_interp_top = top_interp_func(fields_interpolated)

    # Checking the interpolation
    plt.plot(fields_interpolated, mag_interp_bottom)
    plt.plot(fields_interpolated, mag_interp_top)
    plt.title('Checking the interpolation')
    plt.show()

    return fields_interpolated, mag_interp_bottom, mag_interp_top

def calculate_jc(V, a, b, mag_interp_bottom, mag_interp_top):
    """ Function to calculate jc
    
    Args:
    V: volume of the sample
    a: some length parameter I guess
    b: some length parameters I guess
    mag_interp_bottom: numpy array of interpolated magnetisation values for the bottom half of the mawatari loop
    mag_interp_top: numpy array of interpolated magnetisation values for the top half of the mawatari loop

    Returns:
    jc: numpy array of jc values
    """
    # Calculating the magnetisation width between the top and bottom magnetisation values as they now are interpolated based on the same field values
    del_m = mag_interp_top - mag_interp_bottom

    # Converting magnetisation width to jc
    jc = del_m * 20 / ((V*a)*(1-(a/(3*b))))

    return jc

#### Parameters #####
""" These are the parameters you should change for your sample"""

a = 1 # some length parameter I guess
b = 3 # some length parameter I guess
V = 0.003 # volume in some units

sample_name = '65 MJ Kg' # what is the sample called
datafile = r'C:\Users\James\Desktop\magnetisation curves\65 MJkg data.xlsx' # path to the data file

########## Script  ###########
""" This will run the functions defined above - don't touch """
data = read_and_convert(datafile) # read in the data
plot_raw_mawatari_loop(data, sample_name)  # plotting raw mawatari loop
fields_interpolated, mag_interp_bottom, mag_interp_top = interpolate_data(data) # interpolating data
jc = calculate_jc(V, a, b, mag_interp_bottom, mag_interp_top) # Calculating jc
plot_jc_vs_field(fields_interpolated, jc) # Plotting jc vs field

print('Done!')
