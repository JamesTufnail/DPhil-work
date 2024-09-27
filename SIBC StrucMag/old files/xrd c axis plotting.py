"""
Script to plot XRD data from Empyrean X-ray diffractometer.
Input should be saved .csv file of peak and c parameter once lattice parameters have been fitted using excel

e.g.
2theta	a
7.5648	11.67698078499640
15.1275	11.70408644010890
22.7556	11.71395583433560
30.4982	11.71487400769580
38.3858	11.71560294453450
46.4658	11.71649149747700
54.7563	11.72549509803560
72.5841	11.71259370879190
82.1716	11.72114303793750
92.566	11.72349754522870

Set the path to the directory containing the .csv files and the path to save the figures and excel file. 
The script will plot the data and save the figures to the specified directory, also saving and extracting the lattice parameters to an excel file.

NOTE: currently slightly specialsied to the StrucMag experiment as I have 3 of each type of sample with names e.g Fu21-SM1a, Fu21-SM1b, Fu21-SM1c etc. hence some splitting of names using - 

author: James Tufnail
date: 09/04/24

v1.1 
- added functions to plot Nelson-Riley and Bradley-Jay plots
- add option to plot each individually and lay in one 1x3 figure
- append everything to one big dataframe and save to excel
- extract variance and mean of c-axis values for each sample
- plot c lattice parameters for each sample

## TODO: 
- write function to plot FWHM 

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress
import glob


########## Functions ##########
# Define fitting functions
def nelson_riley(two_theta):
    return (np.cos(np.radians(two_theta / 2))**2) / np.sin(np.radians(two_theta / 2)) + (np.cos(np.radians(two_theta / 2))**2) / (np.radians(two_theta / 2))

def bradley_jay(two_theta):
    return (np.cos(np.radians(two_theta / 2))**2)

def misalignment(two_theta):
    return ((np.cos(np.radians(two_theta / 2))**2) / np.sin(np.radians(two_theta / 2)))

def plot_combined(files, plotType):
    """
    Plots data for one separate file over 3 subfigures.
    
    Args:
    files (list): list of file paths to XRD data files
    name (str): name of the plot to be made - to be used in dictionary identification
    
    Returns:
    fig (plt.figure): figure object
    sample_type (str): type of sample"""       

    fig, axs = plt.subplots(1, len(files), figsize=(12,6))  # Create subplots
    sample, a, a_err, r_squared, std, mean = [], [], [], [], [], []
    
    for i, file in enumerate(files):
        data = pd.read_csv(file, delimiter='\t', header = 0)
        sample_name = file.split('\\')[-1].split('.')[0]
        sample_type = file.split('\\')[-1].split('-')[0]

        two_theta = data['2theta']
        # two_theta = data['Pos. [°2θ]']

        scaling_function = fitting_functions[plotType]
        two_theta = scaling_function(two_theta)
        c_axis = data['a']


        # Perform linear regression
        res = linregress(two_theta, c_axis)
        x_min_dic={'c_axis_vs_2theta': 0,
                'nelson_riley' : two_theta.min(),
                'bradley_jay': two_theta.min(),
                'misalignment': 0
                }
        
        x = np.linspace(x_min_dic[plotType], two_theta.max(), 100)
        y = res.slope*x + res.intercept

        # Append data to lists
        sample.append(sample_name)
        a.append(res.intercept)
        a_err.append(1.96*res.intercept_stderr)
        r_squared.append(res.rvalue**2)
        std.append(c_axis.std())
        mean.append(c_axis.mean())
        print(f'Sample {sample_name}, a  {res.intercept}, 95% intercept conf in param {1.96*res.intercept_stderr}, R^2 {res.rvalue**2}, std {c_axis.std()}, mean {c_axis.mean()}')
        
        # plot data
        axs[i].scatter(two_theta, c_axis, label = 'Raw Data')
        axs[i].plot(x, y, linestyle='--', label=f'c(95%)={res.intercept:.3f}±{1.96*res.intercept_stderr:.3f} Å \n R$^2$={res.rvalue**2:.6f}')
        axs[i].set_title(sample_name)
        axs[i].legend(loc='upper right')

    # Set overall x and y labels
    fig.text(0.5, 0.04, x_label_dic[plotType], ha='center', fontsize=12)
    fig.text(0.04, 0.5, 'C-axis Parameter (Å)', va='center', rotation='vertical', fontsize=12)

    fig.suptitle(f'{name_dic[plotType]} for Pristine {sample_type}', fontsize=14)
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 1])  # Adjust subplot layout to make room for labels

    return fig, sample_type, sample, a, a_err, r_squared, std, mean


def plot_single_plot(files, plotType, sample_type):
    
    sample, a, a_err, r_squared, std, mean = [], [], [], [], [], []
    markers = ['o', 'd', '^']
    markers_iter = iter(markers)
    plt.figsize=(12,8)
    
    for file in files:
        data = pd.read_csv(file, delimiter='\t', header = 0)
        # sample_name = file.split('\\')[-1].split('.')[0]
        # sample_type = file.split('\\')[-1].split('-')[0]

        two_theta = data['2theta']
        scaling_function = fitting_functions[plotType]
        two_theta = scaling_function(two_theta)
        c_axis = data['a']

        marker = next(markers_iter)
        plt.scatter(two_theta, c_axis, marker=marker, label = sample_name)

        # Perform linear regression
        res = linregress(two_theta, c_axis)
        x_min_dic={'c_axis_vs_2theta': 0,
                'nelson_riley' : two_theta.min(),
                'bradley_jay': two_theta.min(),
                'misalignment': 0
                }
        
        x = np.linspace(x_min_dic[plotType], two_theta.max(), 100)
        y = res.slope*x + res.intercept

        # Append data to lists
        sample.append(sample_name)
        a.append(res.intercept)
        a_err.append(1.96*res.intercept_stderr)
        r_squared.append(res.rvalue**2)
        std.append(c_axis.std())
        mean.append(c_axis.mean())
        print(f'Sample {sample_name}, a  {res.intercept}, 95% intercept conf in param {1.96*res.intercept_stderr}, R^2 {res.rvalue**2}, std {c_axis.std()}, mean {c_axis.mean()}')
        
        plt.plot(x, y, linestyle='--', label = f'c(95%)={res.intercept:.3f}$\pm${1.96*res.intercept_stderr:.3f} Å \n R$^2$={res.rvalue**2:.6f}')
    
    # Annotate plot
    plt.legend()
    plt.xlabel(x_label_dic[plotType])
    plt.ylabel('c-axis lattice parameter (Å)')
    plt.title(f'{name_dic[plotType]} for Pristine {sample_type}')

    return plt, sample_type, sample, a, a_err, r_squared, std, mean

def save_or_show(fig, save, plotType, sample_name, name):
    """
    Saves or shows the plot depending on the save argument
    
    Args:
    fig (plt.figure): figure object
    save (bool): if true will save to file, if false will show on screen
    name (str): name of the plot to be made e.g. 'c_axis_vs_2theta'
    sample_name (str): name of the sample being plotted
    """

    if save:
        plt.savefig(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\c axis\Figures" + '\\' + sample_name + f'_{plotType}_{name}.png')
        print(f'Saved {plotType} plot for {sample_name}')
        plt.close()
    else:   
        plt.show()
        print(f'Plotted {plotType} curve for {sample_name}')

    return None

def general_extrapolate_plot(files, type, save=False, split_plots=True):

    if split_plots:
        fig, sample_type, sample, a, a_err, r_squared, std, mean = plot_combined(files, plotType=type)
        save_or_show(fig, save, type, sample_type, name='split')
    else:
        fig, sample_type, sample, a, a_err, r_squared, std, mean = plot_single_plot(files, plotType=type)
        save_or_show(fig, save, type, sample_type, name='shared')

    # Open excel file and save
    df = pd.DataFrame({'Sample': sample, 'c-axis': a, 'c-error (95%)': a_err, 'R^2': r_squared, 'std': std, 'mean': mean})
    

    return df, sample_type

def plot_c_axis_parameter(results, sample_list, extrapolation_type):
        # Plotting c axis value for each sample type for all fitting functions
        fig, axs = plt.subplots(1, 3, figsize=(10,4))  # Create subplots

        for i, sample in enumerate(sample_list):
            sliced_sample = results[results.apply(lambda row: row.astype(str).str.contains(sample)).any(axis=1)]

            for extrapolation in extrapolation_type:
                sample_name = sliced_sample[extrapolation]['Sample']
                sample_names = [name.split('-')[-1] for name in sample_name]

                axs[i].errorbar(sliced_sample[extrapolation]['Sample'], sliced_sample[extrapolation]['c-axis'], 
                        yerr=sliced_sample[extrapolation]['c-error (95%)'], 
                        fmt='x',  # Crosses for data points
                        capsize=5,  # Length of the error bar caps
                        label=extrapolation)
            
            axs[i].set_xticks(range(len(sample_names)))
            axs[i].set_xticklabels(sample_names)
            axs[i].set_title(sample)
            axs[0].set_ylabel('c-axis lattice parameter (Å)', fontsize=12)
            axs[1].set_xlabel('Sample', fontsize=12)
            axs[1].legend(loc='upper right')
            
        fig.suptitle('c-axis (95%) lattice parameter for each pristine sample-fitting combination', fontsize=14)
        plt.tight_layout()
        plt.show()

############################# Magic  ########################
name_dic = {
    'c_axis_vs_2theta': 'c-2θ',
    'nelson_riley': 'Nelson-Riley',
    'bradley_jay': 'Bradley-Jay',
    'misalignment': 'Misalignment'
}

x_label_dic = {
    'c_axis_vs_2theta': '2θ (°)',
    'nelson_riley': r'$\frac{{\cos^2(\theta)}}{{\sin(\theta)}} + \frac{{\cos^2(\theta)}}{{\theta}}$',
    'bradley_jay': r'$cos^2(\theta)$',
    'misalignment': r'$\frac{{\cos^2(\theta)}}{{\sin(\theta)}}$'
}

fitting_functions = {
    'c_axis_vs_2theta': lambda x: x,
    'nelson_riley': nelson_riley,
    'bradley_jay': bradley_jay,
    'misalignment': misalignment
}

#################### Script ############################

# csv file(s) destination, obtains list of file names in directory
files = glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\c-axis - new\SM1a")
save_figs = False # if true will save to above file, if false will print on screen

# destination of excel to save parameters
param_file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\python extracted lattice params.xlsx"
save_params = False # if true will save to excel file

# other settings
split = False # if true will plot each sample on a separate figure, if false will plot all samples on one figure
plot_c_axis = True # if true will plot c-axis values for each sample from param file

### Process data and save figures ### comment out if you don't want the fit
_2_theta_df, sample_name = general_extrapolate_plot(files, 'c_axis_vs_2theta', save=save_figs, split_plots=split)
nr_df, sample_name = general_extrapolate_plot(files, 'nelson_riley', save=save_figs, split_plots=split)
# bradley_jay_df, sample_name = general_extrapolate_plot(files, 'bradley_jay', save=save_figs, split_plots=split)
# misalignment_df, sample_name = general_extrapolate_plot(files, 'misalignment', save=save_figs, split_plots=split)


# Save data to excel file
if save_params:
    results = pd.read_excel(param_file, header=[0, 1], index_col=0) # Load existing data
    results = results.dropna(axis=0, ignore_index=True)
    print('Sample name:', sample_name, '\n----------------------------------')

    # Concatenate new dataframes if the sample name doesn't exist
    if not results['2_theta']['Sample'].isin([sample_name]).any() :
        new = pd.concat([_2_theta_df, nr_df, bradley_jay_df, misalignment_df], keys=['2_theta', 'Nelson-Riley', 'Bradley-Jay', 'Misalignment'], axis=1)
        print('New df: \n', '-----------------------------------\n', new.head())
        results = pd.concat([results, new], axis=0, ignore_index=True, sort=False)

        # Write the updated DataFrame to the Excel file
        results.to_excel(param_file)
    print(results)

# Plotting c axis values
if plot_c_axis:
    results = pd.read_excel(param_file, header=[0, 1], index_col=0) # Load existing data
    sample_list = ['Fu21', 'SuNAM', 'SP11']
    extrapolation_type = ['2_theta', 'Nelson-Riley']# , 'Bradley-Jay', 'Misalignment']
    plot_c_axis_parameter(results, sample_list, extrapolation_type)

    