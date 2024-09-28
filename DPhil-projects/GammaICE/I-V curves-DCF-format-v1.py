"""
This version also allows you to run through data from GammaIce rig itself

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from scipy.stats import norm
import glob as glob
import os

################ Functions ###############
def check_data(I, V):

    plt.scatter(I, V, marker='x', s=10)
    plt.xlabel('Current (A)'), plt.ylabel('Voltage ($\mu$V)')
    plt.title('Raw Data')
    plt.show()

    return

def extract_data(path):

    data = pd.read_csv(path, header = 0)
    print(data.head())
    data.dropna(inplace=True)
    data = data.drop(data[data['Measured Current [A]'] < 0].index) # dropping all neg values removes too many data points
    # data = data.drop(data[data['Keithley Voltage [V]'] < - 1e-6].index) # dropping all neg values removes too many data points

    V = data['Keithley Voltage [V]'] * 1e6
    I = data['Measured Current [A]']
    print(V, I)

    return I, V

def power_law(x, Jc, n, c):
    return Vc*(x/Jc)**n + c

def fit_power_law(x, y):
    params, covariance = opt.curve_fit(power_law, x, y)
    Jc, n, c = params
    perr = np.sqrt(np.diag(covariance))
    conf_95_percent = 1.96 * perr
    # print('Confidence intervals (95%) =', conf_95_percent)


    I_fit = np.linspace(I.min(), max(I), 100)
    V_fit = power_law(I_fit, Jc, n, c) - c
    # print('Jc =', Jc, 'n =', n, 'c =', c)
    return I_fit, V_fit, params, conf_95_percent

def I_V_plot(I, V, sample_name, save_path, state, save=False):
    
    I_fit, V_fit, params, conf = fit_power_law(I, V)
    Jc, n, c = params
    Jc_err, n_err, c_err = conf
    V_shift = V - c
    print('Jc =', Jc, 'n =', n, 'c =', c, 'with errors', Jc_err, n_err, c_err)
    
    # Plot raw data
    plt.scatter(I, V_shift, marker='x', s=10,  label = 'Raw Data')

    # Plot fit
    plt.plot(I_fit, V_fit, label=r'Fit: $V = V_c \left(\frac{J}{J_c}\right)^n + c$', color='orange', linewidth=1.5)

    # Annotate plot
    plt.text(9 , 30, 'Constants (95% Confidence)\n'
                    'J$_c$ = {} $\pm$ {:.2e} A\n'
                    'n = {} $\pm$ {}\n'
                    'c = {} $\pm$ {:.2e}'.format(round(Jc, 2), round(Jc_err, 3),
                                                round(n, 2), round(n_err, 2),
                                                round(c, 2), round(c_err, 2)),
            fontsize=8, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))


    plt.axhline(y=Vc,label = 'V$_c$ = 4 $\mu$V', color='grey', linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.xlabel('Current (A)'), plt.ylabel('Voltage ($\mu V$)')
    plt.title('I-V Curve for {}'.format(sample_name))
    plt.legend(loc = 'upper left')

    if save:
        plt.savefig(save_path + '\\' + sample_name + '-' + state + '_I-V.png')
        print('Saved I-V curve for {}'.format(sample_name))
        plt.close()
    else:   
        plt.show()
        print('Plotted I-V curve for {}'.format(sample_name))

    return Jc, n, c, Jc_err, n_err, c_err

def residual_plot(I, V, params, sample_name, save_path, save=False, bin_num = 50):
    
    Jc, n, c = params
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))

    # Calculate residuals
    residuals = V - power_law(I, Jc, n, c)

    # Scatter plot of residuals
    axs[0].scatter(I, residuals, label='Residuals', color='green', s=10)
    axs[0].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Residuals ($\mu V$)'), axs[0].set_xlabel('Current (A)')
    axs[0].set_title('Residuals')

    # Plot histogram of residuals
    axs[1].hist(residuals, bins=bin_num, color='green', label='Residuals', alpha=0.7, density=True)

    # Fit a normal distribution to the residuals
    mu, std = norm.fit(residuals)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    # Plot the PDF
    axs[1].plot(x, p, 'k', linewidth=2,label = 'Fit: $\mu$ = {:.2e}, $\sigma$ = {}'.format(mu, round(std, 2)))

    # Annotate plot
    axs[1].set_xlabel('Residuals ($\mu V$)'), axs[1].set_ylabel('Frequency')
    axs[1].set_title('Histogram with {} bins'.format(bin_num))
    axs[1].legend(loc='upper right')
    fig.suptitle('{}'.format(sample_name))
    plt.tight_layout()

    if save:
        plt.savefig(save_path + '\\' + sample_name + '_residuals.png')
        # plt.savefig(r'C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Figures' + '\\' + sample_name + '_residuals.png')
        print('Saved residual plot for {}'.format(sample_name))
        plt.close()
    else:    
        plt.show()
        print('Plotted residual plot for {}'.format(sample_name))

    return


############### Constants ############
Vc = 4.0  # voltage criterion (in V)
save = True

state = ' Post-ion'
base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\DCF Irradiations\Ic_4\2024-05-08_09_47_57_Ic#4_pre_gamma.csv"
file_name = 'Ic#4 Post-ion'
save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\DCF Irradiations\Ic_4"

############### Script ############
data = pd.read_csv(base_dir, encoding='ISO-8859-1', skiprows=25, header=1, usecols = ['PSU Current (A)', 'UUT Tap (V)']).dropna()
print(data.head())

V = data['UUT Tap (V)'] * 1e6
I = data['PSU Current (A)']

# check_data(I, V)


Jc, n, c, Jc_err, n_err, c_err =  I_V_plot(I, V, file_name, save_path, state=state, save=save) 
residual_plot(I, V, [Jc, n, c], file_name, save_path, save=save)

data_rows = []
data_rows.append([file_name, Jc, n, c, Jc_err, n_err, c_err])

# Create a DataFrame from the list of rows
columns = ['Sample', 'Jc', 'n', 'c', 'Jc_err', 'n_err', 'c_err']
extracted_data = pd.DataFrame(data_rows, columns=columns)
print(extracted_data.head())






















# data_rows = []

# for path, sample_name in zip(files, file_names):
#     sample_name = sample_name + state
#     I, V = extract_data(path)

#     # check_data(I, V)

#     I_fit, V_fit, params, conf = fit_power_law(I, V)

#     Jc, n, c = params
#     Jc_err, n_err, c_err = conf
#     print('Jc =', Jc, 'n =', n, 'c =', c, 'with errors', Jc_err, n_err, c_err)

#     # Plot I-V curve and residuals
#     I_V_plot(I, V, sample_name, save_path, save=save)
#     residual_plot(I, V, params, sample_name, save_path, save=save)

#     # Append data to list of rows
#     data_rows.append([sample_name, Jc, n, c, Jc_err, n_err, c_err])

# # Create a DataFrame from the list of rows
# columns = ['Sample', 'Jc', 'n', 'c', 'Jc_err', 'n_err', 'c_err']
# extracted_data = pd.DataFrame(data_rows, columns=columns)
# extracted_data.to_csv(save_path + '\\' + 'extracted_data.csv', index=False)

# print(extracted_data)

