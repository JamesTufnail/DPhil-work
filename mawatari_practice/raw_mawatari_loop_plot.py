import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp
from scipy.stats import linregress
from scipy.optimize import minimize

############    Defining functions    ############
def find_index_from_temp(data):
    ix=[0]
    
    for i in range(1, len(data)):
        # Compare with the temperature of the previous row
        ix.append(i) if data['Temperature (K)'][i] < data['Temperature (K)'][i-1] - 5 else None

    # ensure last measurement is included
    ix.append(data.index[-1])

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
        plt.savefig(save_path, f'Raw_susceptibility_{sample_name}.png')
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
        plt.savefig(save_path, f'Birr_vs_Magnetic_Field_{sample_name}.png')
        plt.close()
    else:
        plt.show()

    return

def find_tc_interpolation(data, ix, sample_name, show_plot = True):
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
   
    # print('Normal state slope:', slope_norm, '+/- ', 1.96*stderr_norm) # Started trying to calc error in Tc but too involved and seems small anyway

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

############################## ~~~~~~~~ Main Code ~~~~~~~~~ ##############################
sample_name = 'Fu21Gd_SM1a pristine'
bc2 = True
show_plot = False
save = False

# ~~~~~~~~~~~~~~  Read and save locatinos ~~~~~~~~~~~~~~~ #
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Fu21Gd_SM1a\24 01 24\Magnetisation Measurements.dat",
                   header=33, usecols = ['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'], low_memory=False)

save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Fu21Gd_SM1a\Pristine"


# ~~~~~~~~~~ Basic Data Cleaning ~~~~~~~~~~~~~ #
data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)'] * 1e-4)
data.insert(5, 'DC Moment (A m2)', data['DC Moment (emu)'] * 1e-3)
data['Comment'] = data['Comment'].astype(str)

# ~~~~~~~~~~~ Plotting Raw Mawatarai Loop ~~~~~~~~~~~~~ #
ix = find_index_from_temp(data) # Finding indices where the temperature changes
data = clean_data(data, 0.01) # Cleaning data based on std err column to remove spurious data points
plot_raw_mawatari_loop(data, ix, sample_name) # Plotting the raw mawatari loop data


# ~~~~~~~~~~ Plotting Susceptibility Data and Birr ~~~~~~~~~~~~~ #
ix = find_ix_by_sample_offset(data)
tc = find_tc_interpolation(data, ix, sample_name=sample_name, show_plot = show_plot)
# append_tc_to_file(sample, tc)
plot_susceptibility(data, ix, sample_name=sample_name, save_path = save_path, tc = tc, save=save) # plots the susceptibility data for the sample
plot_Birr(data, ix, sample_name=sample_name, save_path=save_path, bc2=bc2, save=save)

