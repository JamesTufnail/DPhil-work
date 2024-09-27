"""
FULL PPMS ANALYSIS SCRIPT
Author: James Tufnail
Date: 02/08/2024

This script is designed to analyse the data from the PPMS system. The script will perform the following tasks:
1. Open the data file
2. Clean the data
3. Plot the raw Mawatari loop data
4. Plot the susceptibility data
5. Plot the Birr data
6. Find the transition temperature

Data format:
paths to files are given as strings 
- magnetisation_path: path to the magnetisation data file
- susceptibility_path: path to the susceptibility data file


TODO for version 1.1:
- Fix bug - some interp functions don't work and produce a Tc = 90.0000K value. Fix by generalising the interp ranges to work based on percentages no indices (like in GammaICE scripts)
- combine the functions for opening the data into one function that can be used for both magnetisation and susceptibility data





"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp
from scipy.stats import linregress
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d
from sklearn.preprocessing import MinMaxScaler

from functions import *

############    Defining functions    ############
def find_index_from_temp(data):
    ix=[0]
    
    for i in range(1, len(data)):
        # Compare with the temperature of the previous row
        ix.append(i) if data['Temperature (K)'][i] < data['Temperature (K)'][i-1] - 5 else None

    # ensure last measurement is included
    ix.append(data.index[-1])

    return ix


def find_ix_by_sample_offset(data):
    """
    Is used in for Susceptibility measurements.
    Function to find the index of the data where the sample offset is recorded. 
    This is used to index through the data to find the start of each measurement

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

def clean_data(data, std_err):
# Cleaning data based on std err column to remove spurious data points
    data.loc[data['DC Std. Err. (emu)'] > std_err, 'DC Moment (A m2)'] = None
    return data

def plot_raw_mawatari_loop(data, ix, sample_name):
    """
    Function to plot the raw mawatari loop data for a given sample
    
    Parameters:
    data (pd.DataFrame): Dataframe containing the data
    ix (list): List of indices where the temperature changes
    sample_name (str): Name of the sample
    
    Returns:
    None
    """
    temp, field = [], []
    plt.figure(figsize=(8, 4))
            
    for index, i in enumerate(ix):
        if index < len(ix) - 1:
            start = ix[index]
            end = ix[index + 1] 
            temp.append(data['Temperature (K)'][i].round(0))
            # print('start:', start, 'end:', end)
            # print('Temperature:', temp, 'Field:', field)
            
            plt.scatter(data['Magnetic Field (T)'][start:end], data['DC Moment (A m2)'][start:end], label = '{} K'.format(temp[index]), s=2.5)


    plt.legend(loc='upper right')
    plt.title('Magnetisation data for {}'.format(sample_name))
    plt.xlabel('Magnetic Field (T)')
    plt.ylabel('Magnetisation (A m$^2$)')
    plt.show()

    return print('Plotted raw mawatari loop for {}'.format(sample_name))


def plot_susceptibility(data, ix, sample_name, tc, save_path, save=False):

# Plotting the susceptibility and recording Birr
    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8, 6))

    # Initialising lists to store magnetic field
    field = []

    # set number of symbols
    markers = ['o', '+', '*', 's', '1', 'D']

    for index, (i, marker) in enumerate(zip(ix, markers)):
        if index < len(ix) - 1:
            start = ix[index]
            end = ix[index + 1] 
            field.append(abs(data['Magnetic Field (T)'][i].round(2)))

            # plot normal and imaginary parts of the susceptibility
            axs[1].scatter(data['Temperature (K)'][start:end], data["AC X'  (emu/Oe)"][start:end],
                            label = '{} T'.format(field[index]), marker = marker, s=10)
            axs[0].scatter(data['Temperature (K)'][start:end], data['AC X" (emu/Oe)'][start:end],
                            label = '{} T'.format(field[index]), marker=marker, s=10)

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
        plt.savefig(f'{save_path}/Raw_susceptibility_{sample_name}.png')
        plt.close()
    else:
        plt.show()

    return 

def plot_Birr(data, ix, sample_name, save_path, save=False, Tc=None):

    field, Birr, Bc2 = [], [], []
    for index, i in enumerate(ix):
        if index < len(ix) - 1:
            start = ix[index]
            end = ix[index + 1] 
            field.append(abs(data['Magnetic Field (T)'][i].round(2)))

            # Finding Birr as the temperature at which the real part of the susceptibility is maximised
            for j in range(start, end):
                if data['AC X" (emu/Oe)'][j] == max(data['AC X" (emu/Oe)'][start:end]):
                    Birr.append(data['Temperature (K)'][j])

            # Finding Bc2
            ac_90k = data["AC X'  (emu/Oe)"][np.argmin(abs(data['Temperature (K)'][start:end] - 90))]
            ac_30k = data["AC X'  (emu/Oe)"][np.argmin(abs(data['Temperature (K)'][start:end] - 30))]
            ac_99_threshold = ac_30k + 0.99 * (ac_90k - ac_30k)
            # print('AC 90K:', ac_90k, 'AC 30K:', ac_30k, 'Threshold:', ac_99_threshold)

            closest_value = None
            closest_diff = float('inf')
            for k in range(start, end):
                diff = abs(data["AC X'  (emu/Oe)"][k] - ac_99_threshold)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_value = data['Temperature (K)'][k]

            if closest_value is not None:
                Bc2.append(closest_value)

    print('Bc2', Bc2)
    print('Birr', Birr)
    print('Field', field)

    # plotting 
    plt.scatter(Bc2, field, label='Bc2')
    plt.scatter(Birr, field, label='Birr')
 
    x = Bc2
    # print('x', x)
    # print('field', field)
    # print('Tc', Tc)

    ##TODO: fit BC2 data to extract the Bc2 value based on G. Fuchs et al 
    # NOTE THAT p0 ARE FOR THE INITIAL GUESS OF THE PARAMETERS, not of the function
    popt, pcov = curve_fit(lambda x, Bc2_0, alpha: Bc2_model(x, Tc, alpha, Bc2_0),
                             xdata=Bc2, ydata=field,
                             p0=[100, 1.5], 
                             bounds=([0, 1], [1000, 5]),
                             maxfev=5000)
    Bc2_0, alpha = popt
    print('Fitted Bc2 data with Fuchs et al model: Bc2_0', Bc2_0, 'Alpha:', alpha)
    

    x_interp = np.linspace(65, 90, 1000)
    Hc2_fit = Bc2_model(x_interp, Tc, alpha, Bc2_0)
    Tc = Tc
    # plt.plot(x_interp, Hc2_fit, label=rf'$B_{{c2}} = {Bc2_0:.2f}\left(1 - \frac{{T}}{{{Tc:.2f}}}\right)^{{{alpha:.2f}}}$')


    # annotate plot
    plt.title(f'Birr(T) for {sample_name} sample')
    plt.xlabel('Temperature (K)'), plt.ylabel('Magnetic Field (T)')
    plt.legend()
    plt.ylim(bottom=0)

    if save:
        plt.savefig(f'{save_path}/Birr_{sample_name}.png')
        plt.close()
    else:
        plt.show()

    return

def Bc2_model(x, Tc, alpha, Bc2_0):
    return Bc2_0*(1 - (x/Tc)**alpha)


"""def find_tc_interpolation(data, ix, sample_name, show_plot = True):
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
    slope_norm, intercept_norm, r, p, stderr_norm = linregress(temp_fit_norm, sus_fit_norm)
   

    x_norm = np.linspace(temp.iloc[0], temp.iloc[-1], 10000)
    
    # Fitting transition region
    slope_trans, intercept_trans, r, p, se_trans = linregress(temp_fit_trans, sus_fit_trans)
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
        plt.title(f'{sample_name}')
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

def find_tc_interp_new(data, ix, LowerCriterion, UpperCriterion):

    # extract indices and data
    start, end = ix[0], ix[1] # Ix for all
    temp, sus = data['Temperature (K)'][start:end], data["AC X'  (emu/Oe)"][start:end]

    # normalise susceptibility data
    # scaler = MinMaxScaler()
    # sus_norm = scaler.fit_transform(sus.values.reshape(-1, 1)).flatten()

    # Interpolating the temp data
    sus_func = interp1d(temp, sus, kind='cubic') # find interp fucntion based on orgiinal data
    temp_interp = np.linspace(temp.iloc[0], temp.iloc[-1], 500000) # choose new x  values for interpolation
    sus_interp = sus_func(temp_interp) # interpolate the data

    # setting region interp
    linear_region_t, linear_region_sus = temp_interp[-10000:], sus_interp[-10000:]
    normal_region_range = temp_interp[:10000]

    # Fitting normal region
    slope_norm, intercept_norm, r, p, stderr_norm = linregress(linear_region_t, linear_region_sus)
    y = slope_norm * normal_region_range + intercept_norm
    x_norm = np.linspace(temp.iloc[0], temp.iloc[-1], 10000)





    temp_lower = np.ones(len(temp_interp)) *  LowerCriterion # setting temp_lower to be a straigh line of 0.1
    temp_upper = np.ones(len(temp_interp)) *  UpperCriterion # setting temp_upper to be a straight line of 0.9

    # plotting the data
    plt.scatter(temp_interp, sus_interp, label='Interpolated AC Susceptibility')
    plt.plot(x_norm, y, label='Fitted Normal Region')

    plt.show()



    return
"""
def find_tc_derivative(data, ix):
    """
    Function to extract the deritiave Tc (i.e. the turning point of the derivative of the susceptibility data)

    Parameters:
    data (pd.DataFrame): Dataframe containing the data
    ix (list): List of indices where the temperature changes

    Returns:
    tc (float): Transition temperature 
    
    """

    # extracting indices
    start, end = ix[0], ix[1] # Ix for all

    # extracting data
    temp, sus = data['Temperature (K)'][start:end], data["AC X'  (emu/Oe)"][start:end]

    # normalising the susceptiility data
    scaler = MinMaxScaler()
    sus_norm = scaler.fit_transform(sus.values.reshape(-1, 1)).flatten()

    # Interpolating the temp data
    sus_func = interp1d(temp, sus_norm, kind='cubic') # find interp fucntion based on orgiinal data
    temp_interp = np.linspace(temp.iloc[0], temp.iloc[-1], 500000) # choose new x  values for interpolation
    sus_interp = sus_func(temp_interp) # interpolate the data

    # calculating derivative of susceptibility data (dX/dT) 
    derivative = np.gradient(sus_interp, temp_interp) 

    # Finding the maximum of the derivative
    tc = temp_interp[np.argmax(derivative)]

    # plot derivative and data
    plt.plot(temp_interp, derivative, label='dX/dT')
    plt.plot(temp_interp, sus_interp, label = 'Interpolated AC Susceptibility')
    plt.scatter(temp, sus_norm, label='AC Susceptibility')
    plt.scatter(tc, sus_interp[np.argmax(derivative)], marker='x', label='Tc={}'.format(tc))
    plt.legend()
    plt.title('Deriative Tc of Normalised AC Susceptibility')

    plt.show()

    print('derivative Tc finished. Tc = {tc} K')
    return tc


def open_susceptibility_data(data_path, sample_name):
    """
    Function to open the data for a specific sample. The function uses the glob module to search for the data in the specified path

    Parameters:
    data_path (str): Path to the data file
    sample_name (str): Name of the sample to search for

    Returns:
    data (pd.DataFrame): Dataframe containing the data for the specified sample
    """

    # # Opening file path
    # data_file_pattern = os.path.join(data_path, sample_name, 'Irr0', 'PPMS Data') + '\**\Susceptibility_Measurements.dat'
    # file_path = glob.glob(data_file_pattern, recursive=True)[0]
    # print('Sample is:', sample_name)
    # print('Data path is:', file_path)

    # # Saving file path
    # save_path_pattern = os.path.join(data_path, sample_name, 'Irr0', 'PPMS Data')
    # save_path = glob.glob(save_path_pattern + '\*', recursive=True)[0]
    # print('Save path is:', save_path)
    # # print(save_path_pattern)


    # Extract the data
    data = pd.read_csv(data_path, header=33, usecols=[0,2,3,10,11])
    data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)']/10000)
    data['Comment'] = data['Comment'].astype(str)
    print('Data opened for:', sample_name)
    print(data.head())

    return data

############################## ~~~~~~~~ Main Code ~~~~~~~~~ ##############################
sample_name = 'SP11-SM3c 1.6 mdpa'
show_plot = False
save = False

# LowerCriterion = 0.
# UpperCriterion = 0.9

# ~~~~~~~~~~~~~~  Read and save locatinos ~~~~~~~~~~~~~~~ #
magnetisation_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Sp11_SM3c\24 07 16\Magnetisation Measurements.dat"
susceptibility_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Sp11_SM3c\24 07 16\Susceptibility_Measurements.dat"
save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Figures"


# ~~~~~~~~~~ Basic Data Cleaning ~~~~~~~~~~~~~ #
mag_data = pd.read_csv(magnetisation_path, header=33, usecols = ['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'],
                                  low_memory=False)
mag_data.insert(3, 'Magnetic Field (T)', mag_data['Magnetic Field (Oe)'] * 1e-4)
mag_data.insert(5, 'DC Moment (A m2)', mag_data['DC Moment (emu)'] * 1e-3)
mag_data['Comment'] = mag_data['Comment'].astype(str)

# ~~~~~~~~~~~ Plotting Raw Mawatarai Loop ~~~~~~~~~~~~~ #
ix = find_index_from_temp(mag_data) # Finding indices where the temperature changes
data = clean_data(mag_data, 0.01) # Cleaning data based on std err column to remove spurious data points
plot_raw_mawatari_loop(data, ix, sample_name) # Plotting the raw mawatari loop data


# ~~~~~~~~~~ Plotting Susceptibility Data and Birr ~~~~~~~~~~~~~ #
data = open_susceptibility_data(susceptibility_path, sample_name=sample_name)
ix = find_ix_by_sample_offset(data)
deriv_tc = find_tc_derivative(data, ix)

plot_susceptibility(data, ix, sample_name=sample_name, save_path = save_path, tc = deriv_tc, save=save) # plots the susceptibility data for the sample
plot_Birr(data, ix, sample_name=sample_name, save_path=save_path, save=save, Tc=deriv_tc) # plots the Birr data for the sample

# ~~~~~~~~~~~~~~~~~~ Saving Tc ~~~~~~~~~~~~~~~~~~~~~ #
# tc_data = pd.DataFrame({'Sample': sample_name, 'Tc': deriv_tc}, index=[0])
tc_data = pd.read_excel('Tc_deriv_data.xlsx')
new_tc = pd.DataFrame({'Sample': sample_name, 'Tc': deriv_tc}, index=[0])
tc_data = pd.concat([tc_data, new_tc], ignore_index=True)
print(tc_data)
tc_data.to_excel('Tc_deriv_data.xlsx', index=False)