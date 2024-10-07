"""
xrd c-axis plotting v2.py
author: James Tufnail
date: 19/06/2024

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



Actions:
- Choose plotting functions (NR is the best) 
- Change file locations to find .csv files of 2theta-a data
- Change file locations to select where to save figs and excel file


TODO:
- Fix plot to show all fiting functions and their errors on one plot 

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress
import glob

#### File Locations ####

files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\XRD\Annealed-xrd\#an-01\#an-01-peaks.txt"]
sample_names = [' O2 Annealed']
sample_type = ' SuNAM21Gd '

# sample_type = 'Fu21Gd'
# sample_names = ['SM1a', 'SM1b', 'SM1c']
# files = glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Ion 1 XRD\c-axis\SM1*.txt")

# sample_type = 'SuNAM21Gd'
# sample_names = ['SM2a', 'SM2b', 'SM2c']
# files = glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Ion 1 XRD\c-axis\SM2*.txt")

# sample_type = 'SP11Gd'
# sample_names = ['SM3a', 'SM3b', 'SM3c']
# files = glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Ion 1 XRD\c-axis\SM3*.txt")

# destination of the excel file to save dataframe to
param_file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\python extracted lattice params.xlsx"
fig_destination = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Ion 1 XRD\Figures"

####### Magic ###########
save_fig = False # Setting to True will save the figures
save_params = False # Setting to True will save the parameters to the excel file

plotType = 'nelson_riley'


############### Define fitting functions #################
def nelson_riley(two_theta):
    return (np.cos(np.radians(two_theta / 2))**2) / np.sin(np.radians(two_theta / 2)) + (np.cos(np.radians(two_theta / 2))**2) / (np.radians(two_theta / 2))

def bradley_jay(two_theta):
    return (np.cos(np.radians(two_theta / 2))**2)

def misalignment(two_theta):
    return ((np.cos(np.radians(two_theta / 2))**2) / np.sin(np.radians(two_theta / 2)))

################# Define plotting functions ###############

def plot_single_plot(files, plotType, sample_names, sample_type, save_fig=False, save_params=False):
    
    """
    PLOTS INDIVIDUAL SAMPLES ON SEPARATE PLOTS

    This reads the .csv files from the list of files and plots the c-axis vs the fitting function. 
    It then performs a linear regression on the data and plots the line of best fit. 
    It also saves individual plots if save_fig=True. It returns the plot and a dataframe of the results.
    
    Parameters:
    files (list): list of file paths to the .csv files
    plotType (str): the type of plot to be made. Options are 'c_axis_vs_2theta', 'nelson_riley', 'bradley_jay', 'misalignment'
    sample_names (list): list of sample names
    sample_type (str): the type of sample
    save_fig (bool): whether to save the figure
    save_params (bool): whether to save the parameters to an excel file
    """
    sample, a, a_err, r_squared, std, mean, plot_type = [], [], [], [], [], [], []
    markers = ['o', 'd', '^']
    markers_iter = iter(markers)
    plt.figsize=(12,8)
    
    for file, sample_name in zip(files, sample_names):
        data = pd.read_csv(file, delimiter='\t', header = 0)
        print(data.head())

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
        sample.append(sample_type + '-' + sample_name)
        a.append(res.intercept)
        a_err.append(1.96*res.intercept_stderr)
        r_squared.append(res.rvalue**2)
        std.append(c_axis.std())
        mean.append(c_axis.mean())
        plot_type.append(f'{plotType}')
         
        plt.plot(x, y, linestyle='--', label = f'c(95%)={res.intercept:.3f}$\pm${1.96*res.intercept_stderr:.3f} Å \n R$^2$={res.rvalue**2:.6f}')
    
        # Annotate plot
        plt.legend()
        plt.xlabel(x_label_dic[plotType])
        plt.ylabel('c-axis lattice parameter (Å)')
        plt.title(f'{name_dic[plotType]} for {sample_type}-' + sample_name )

        if save_fig:
            plt.savefig(fig_destination + '\\' + sample_type + '-' + sample_name + ' ' + f'{plotType}' + '.png')
            print(f'Saved {plotType} plot for {sample_name}')
            plt.close()
        else:   
            plt.show()
            print(f'Plotted {plotType} curve for {sample_name}') 

    # Producing results df
    results_df = pd.DataFrame({'Sample': sample, 'Type': plot_type,'c-axis': a, 'c-error (95%)': a_err, 'R^2': r_squared, 'std': std, 'mean': mean})
    print(pd.DataFrame({'Sample': sample, 'Type': plot_type,'c-axis': a, 'c-error (95%)': a_err, 'R^2': r_squared, 'std': std, 'mean': mean}))
    if save_params:
        # Open excel file and save
        results = pd.read_excel(param_file, header=0, index_col=0) # Load existing data

        # Concatenate new dataframes if the sample name doesn't exist
        results = pd.concat([results, results_df], axis=0, ignore_index=True, sort=False)

        # Write the updated DataFrame to the Excel file
        results.to_excel(param_file)   

    return plt, results_df
   
def plot_combined_plot(files, plotType, sample_names, sample_type, save_fig=False, save_params=False):
    
    """
    PLOTS ALL SAMPLES ON THE SAME PLOT

    This reads the .csv files from the list of files and plots the c-axis vs the fitting function. 
    It then performs a linear regression on the data and plots the line of best fit. 
    It also saves the plots if save_fig=True. 
    
    Parameters:
    files (list): list of file paths to the .csv files
    plotType (str): the type of plot to be made. Options are 'c_axis_vs_2theta', 'nelson_riley', 'bradley_jay', 'misalignment'
    sample_names (list): list of sample names
    sample_type (str): the type of sample
    save_fig (bool): whether to save the figure
    save_params (bool): whether to save the parameters to an excel file
    """
    sample, a, a_err, r_squared, std, mean, plot_type = [], [], [], [], [], [], []
    markers = ['o', 'd', '^']
    markers_iter = iter(markers)
    plt.figsize=(12,8)
    
    for file, sample_name in zip(files, sample_names):
        data = pd.read_csv(file, delimiter='\t', header = 0)
        print(data.head())

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
        sample.append(sample_type + '-' + sample_name)
        a.append(res.intercept)
        a_err.append(1.96*res.intercept_stderr)
        r_squared.append(res.rvalue**2)
        std.append(c_axis.std())
        mean.append(c_axis.mean())
        plot_type.append(f'{plotType}')
         
        plt.plot(x, y, linestyle='--', label = f'c(95%)={res.intercept:.3f}$\pm${1.96*res.intercept_stderr:.3f} Å \n R$^2$={res.rvalue**2:.6f}')
    
        # Annotate plot
        plt.legend()
        plt.xlabel(x_label_dic[plotType])
        plt.ylabel('c-axis lattice parameter (Å)')
        plt.title(f'{name_dic[plotType]} for Pristine {sample_type}')

    if save_fig:
        plt.savefig(fig_destination + '\\' + sample_type + ' ' + f'{plotType}' + '-combined.png')
        print(f'Saved {plotType} plot for {sample_name}')
        plt.close()
    else:   
        plt.show()
        print(f'Plotted {plotType} curve for {sample_name}') 

        # Producing results df
    results_df = pd.DataFrame({'Sample': sample, 'Type': plot_type,'c-axis': a, 'c-error (95%)': a_err, 'R^2': r_squared, 'std': std, 'mean': mean})

    if save_params:
        # Open excel file and save
        results = pd.read_excel(param_file, header=0, index_col=0) # Load existing data

        # Concatenate new dataframes if the sample name doesn't exist
        results = pd.concat([results, results_df], axis=0, ignore_index=True, sort=False)

        # Write the updated DataFrame to the Excel file
        results.to_excel(param_file)   

    return plt, results_df

# def plot_c_axis_parameter(results, sample_list, extrapolation_type):
        
#         # Plotting c axis value for each sample type for all fitting functions
#         fig, axs = plt.subplots(1, 3, figsize=(10,4))  # Create subplots

#         for i, sample in enumerate(sample_list):
                
#             if results['Sample']

#                 axs[i].errorbar(sliced_sample[extrapolation]['Sample'], sliced_sample[extrapolation]['c-axis'], 
#                         yerr=sliced_sample[extrapolation]['c-error (95%)'], 
#                         fmt='x',  # Crosses for data points
#                         capsize=5,  # Length of the error bar caps
#                         label=extrapolation)
            
#             axs[i].set_xticks(range(len(sample_names)))
#             axs[i].set_xticklabels(sample_names)
#             axs[i].set_title(sample)
#             axs[0].set_ylabel('c-axis lattice parameter (Å)', fontsize=12)
#             axs[1].set_xlabel('Sample', fontsize=12)
#             axs[1].legend(loc='upper right')
            
#         fig.suptitle('c-axis (95%) lattice parameter for each pristine sample-fitting combination', fontsize=14)
#         plt.tight_layout()
#         plt.show()

############################# Dictionairies  ########################
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

###############
"""This section is where you choose to plot individually or all on a combined plot"""
plt, results_df = plot_single_plot(files, plotType, sample_names, sample_type, save_fig=save_fig, save_params=save_params)
# plt, results_df = plot_combined_plot(files, plotType, sample_names, sample_type, save_fig=save_fig, save_params=save_params)


""" Below currently doesn't work..."""
# results = pd.read_excel(param_file, header=[0, 1], index_col=0) # Load existing data
# print(results.head())
# sample_list = ['Fu21', 'SuNAM', 'SP11']
# extrapolation_type = ['2_theta', 'Nelson-Riley' , 'Bradley-Jay', 'Misalignment']
# # plot_c_axis_parameter(results, sample_list, extrapolation_type)
